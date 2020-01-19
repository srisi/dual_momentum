from dual_momentum.dm_component import DualMomentumComponent
from IPython import embed
from dual_momentum.ticker_data import TickerData
from dual_momentum.fred_data import load_fred_data
import numpy as np

class DualMomentumComposite:
    """
    DualMomentumComposite simulates multiple DM components, e.g. reits and equities

    """

    def __init__(self, parts: list, money_market_holding: str, momentum_leverages: dict,
                 tax_config: dict, start_date: str, leverage: float,
                 borrowing_cost_above_libor: float):


        if abs(sum([x['weight'] for x in parts]) - 1) > 0.0001:
            raise ValueError('Total weights assigned need to sum to one.')

        if not len([x['name'] for x in parts]) == len(set([x['name'] for x in parts])):
            raise ValueError('The name of all parts need to be unique. Current: '
                             f'{[x["name"] for x in parts]}.')

        if not 0 < leverage < 1000:
            raise ValueError(f'Leverage has to be between 0 and 1000, not {leverage}.')

        if leverage > 1 and (borrowing_cost_above_libor is None or borrowing_cost_above_libor < 0):
            raise ValueError(f'If using leverage, borrowing_cost_above_libor needs to be a float, '
                             f'e.g. 1.5 -> 1.5% above libor. Current: {borrowing_cost_above_libor}')


        self.components = []
        for part in parts:
            if part['weight'] < 0 or part['weight'] > 1:
                raise ValueError(f'Weight for part {part["name"]} has to be between 0 and 1')
            component = DualMomentumComponent(
                name=part['name'], ticker_list=part['ticker_list'], tax_config=tax_config,
                lookback_months=part['lookback_months'], max_holdings=part['max_holdings'],
                use_dual_momentum=part['use_dual_momentum'], start_date=start_date,
                money_market_holding=money_market_holding, weight=part['weight']
            )
            self.components.append(component)

        # self.parts = parts
        self.money_market_holding = money_market_holding
        self.momentum_leverages = momentum_leverages
        self.tax_config = tax_config
        self.start_date = start_date
        self.leverage = leverage
        self.borrowing_cost_above_libor = borrowing_cost_above_libor

        self.libor = load_fred_data('libor_rate')

        self.simulation_finished = False


    def run_multi_component_dual_momentum(self):

        self.df = TickerData('ONES').data_monthly
        df = self.df
        df.drop(['Adj Close', 'Close'], inplace=True, axis=1)
        df['cash_portion'] = 0.0
        df['performance_pretax'] = 0.0
        df['taxes'] = 0.0

        # each money market holding works like a buy and hold component
        for mm_holding in ['TLT', 'VGIT']:
            component = DualMomentumComponent(
                name=mm_holding, ticker_list=[mm_holding], tax_config=self.tax_config,
                lookback_months=12, max_holdings=1, use_dual_momentum=False, start_date=self.start_date,
                money_market_holding=mm_holding
            )
            component.run_dual_momentum()

            df[f'{mm_holding}_performance_pretax'] = component.df['performance_pretax']
            df[f'{mm_holding}_performance_posttax'] = component.df['performance_posttax']
            df[f'{mm_holding}_taxes'] = component.df['taxes']

        for component in self.components:
            component.run_dual_momentum()

            df[f'{component.name}_holding'] = component.df['holding']
            df[f'{component.name}_performance_pretax'] = component.df['performance_pretax']
            df[f'{component.name}_taxes'] = component.df['taxes']
            df[f'{component.name}_performance_posttax'] = component.df['performance_posttax']

            df['performance_pretax'] += component.weight * component.df['performance_pretax']
            df['taxes'] += component.weight * component.df['taxes']


        df['leverage'] = 0.0
        df['cash'] = 0.0
        df['mmh'] = self.money_market_holding
        df['ret_ann_tbil'] = 0.0
        df['leverage_costs'] = 0
        df['lev_performance_pretax'] = 1.0
        df['taxes_month'] = 0.0
        df['taxes_due_total'] = 0.0
        df['taxes_paid'] = 0.0
        df['lev_performance_posttax'] = 10000
        df['lev_dd'] = 0.0
        df['performance_pretax_min_tbil'] = 1.0


        for idx, (date, row) in enumerate(self.df.iterrows()):
            # skip until all dual momentum components have enough lookback data
            if idx < max([c.lookback_months for c in self.components if c.use_dual_momentum]):
                continue

            year, month = date

            prev_total = df.at[df.index[idx - 1], 'lev_performance_posttax']
            # months_for_lev would go here...

            # calculate leveraged return and update cash portion accordingly
            lev_performance_pretax = self.leverage * (row['performance_pretax'] - 1) + 1
            percentage_cash = 1 - ((1 - row['cash_portion']) * self.leverage)

            taxes_month = self.leverage * row['taxes'] * prev_total

            # if we hold some cash, put it now into the money market holding
            if percentage_cash >= 0:
                #TODO: implement other money market holding options
                if self.money_market_holding in ['SHY', 'VGIT', 'IEF', 'TLT', 'BOND', 'BND',
                                                 'ONES']:
                    mm_pretax = row[f'{self.money_market_holding}_performance_pretax'] - 1
                    lev_performance_pretax += percentage_cash * mm_pretax
                    taxes_month += row[f'{self.money_market_holding}_taxes'] * percentage_cash * \
                                   prev_total
                    df.at[date, 'mmh'] = self.money_market_holding

            # otherwise, we are borrowing money for leverage -> account for that
            else:
                leverage_percentage = -percentage_cash
                libor = self.libor[date]

                # monthly_borrowing_rate is the monthly borrowing cost
                # e.g. 0.01 -> leverage costs 1% of the the leveraged capital per month
                monthly_borrowing_rate = ((libor + self.borrowing_cost_above_libor) / 100) ** (1/12)
                monthly_borrowing_rate -= 1

                # we only pay leverage cost for the percentage of the portfolio that's leveraged
                leverage_cost = leverage_percentage * monthly_borrowing_rate
                df.at[date, 'leverage_cost'] = leverage_cost
                lev_performance_pretax -= leverage_cost

            taxes_due_total = taxes_month + df.at[df.index[idx - 1], 'taxes_due_total']
            taxes_paid = 0

            # calculate returns after taxes
            lev_performance_posttax = lev_performance_pretax * prev_total
            # if end of january (200x, 12), pay taxes
            if month == 12 and taxes_due_total > 0:
                lev_performance_posttax -= taxes_due_total
                taxes_paid = taxes_due_total
                taxes_due_total = 0

            df.at[date, 'lev_performance_pretax'] = lev_performance_pretax
            df.at[date, 'taxes_month'] = taxes_month
            df.at[date, 'taxes_due_total'] = taxes_due_total
            df.at[date, 'taxes_paid'] = taxes_paid
            df.at[date, 'lev_performance_posttax'] = lev_performance_posttax
            df.at[date, 'leverage'] = self.leverage
            df.at[date, 'cash'] = max(0, percentage_cash)


        self.simulation_finished = True

    def get_cumulative_performance(self, pre_or_posttax='pretax'):

        if not self.simulation_finished:
            raise ValueError('Can only calculate performance after '
                             'run_multi_component_dual_momentum')
        if not 'performance_pretax_cumulative' in self.df:
            self.df['performance_pretax_cumulative'] = np.cumprod(self.df['lev_performance_pretax'])
            self.df['performance_posttax_cumulative'] = np.cumprod(
                self.df['lev_performance_posttax'])

        if pre_or_posttax == 'pretax':
            return self.df['performance_pretax_cumulative']
        else:
            return self.df['performance_posttax_cumulative']

    def get_result_json(self):

        import json


        if self.simulation_finished:
            self.get_cumulative_performance('pretax')

            self.df['prev_total'] = self.df.performance_pretax_cumulative.shift(1).fillna(1)

            values = []
            for idx, (date, row) in enumerate(self.df.iterrows()):
                # skip until all dual momentum components have enough lookback data
                if idx < max([c.lookback_months for c in self.components if c.use_dual_momentum]):
                    continue
                # skip last row
                if idx == len(self.df) - 1:
                    continue

                values.append({
                    'date': date,
                    'value_start': row['prev_total'],
                    'value_end': row['performance_pretax_cumulative']
                })

                with open('temp_data.json', 'w') as out:
                    json.dump(values, out)


            return values







if __name__ == '__main__':

    tax_config = {'st_gains': 0.35, 'lt_gains': 0.15, 'federal_tax_rate': 0.22,
                  'state_tax_rate': 0.12}
    money_market_holding = 'VGIT'
    start_date = '1980-01-01'
    leverage = 2
    borrowing_cost_above_libor = 1.5
    parts = [
        {
            'name': 'equities',
            'ticker_list': ['VTI', 'VWO'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings':1, 'weight': 0.5
        },
        {
            'name': 'SP500',
            'ticker_list': ['SPY'],
            'lookback_months': 12, 'use_dual_momentum': False, 'max_holdings': 1, 'weight': 0.5
        }
    ]

    momentum_leverages = {
       'months_for_lev': 3,
                    0.80: -0.3, 0.85: -0.3, 0.90: -0.2, 0.95: -0.2,
        1.30:  0.2, 1.20:  0.1, 1.15:  0.1, 1.10:  0.0, 1.05:  0.0
    }

    dm = DualMomentumComposite(parts=parts, money_market_holding=money_market_holding,
                               momentum_leverages=momentum_leverages, tax_config=tax_config,
                               start_date=start_date,
                               leverage=leverage,
                               borrowing_cost_above_libor=borrowing_cost_above_libor)
    dm.run_multi_component_dual_momentum()
    dm.get_result_json()



