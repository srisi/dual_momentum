from dm_component import DualMomentumComponent
from IPython import embed
from ticker_data import TickerData

class DualMomentumComposite:
    """
    DualMomentumComposite simulates multiple DM components, e.g. reits and equities

    """

    def __init__(self, parts: list, money_market_holding: str, momentum_leverages: dict,
                 tax_config: dict, start_date: str):


        if abs(sum([x['weight'] for x in parts]) - 1) > 0.0001:
            raise ValueError('Total weights assigned need to sum to one.')

        self.components = []
        for part in parts:
            if part['weight'] < 0 or part['weight'] > 1:
                raise ValueError(f'Weight for part {part["name"]} has to be between 0 and 1')
            component = DualMomentumComponent(
                name=part['name'], ticker_list=part['ticker_list'], tax_config=tax_config,
                lookback_months=part['lookback_months'], max_holdings=part['max_holdings'],
                use_dual_momentum=part['use_dual_momentum'], start_date=start_date,
                money_market_holding=money_market_holding
            )
            component.run_dual_momentum()
            self.components.append(component)

        self.parts = parts
        self.money_market_holding = money_market_holding
        self.momentum_leverages = momentum_leverages
        self.tax_config = tax_config
        self.start_date = start_date


    def run_multi_component_dual_momentum(self):

        self.df = TickerData('ONES').data_monthly
        self.df.drop(['Adj Close', 'Close'], inplace=True, axis=1)
        self.df['cash_portion'] = 0.0
        self.df['performance_pretax'] = 0.0
        self.df['taxes'] = 0.0

        # each money market holding works like a buy and hold component
        mm_holding = 'VGIT'
        component = DualMomentumComponent(
            name=mm_holding, ticker_list=[mm_holding], tax_config=self.tax_config,
            lookback_months=12, max_holdings=1, use_dual_momentum=False, start_date=self.start_date,
            money_market_holding=mm_holding
        )
        component.run_dual_momentum()

        self.df[f'{mm_holding}_performance_pretax'] = component.df['performance_pretax']
        self.df[f'{mm_holding}_performance_posttax'] = component.df['performance_posttax']
        self.df[f'{mm_holding}_taxes'] = component.df['taxes']



        embed()

if __name__ == '__main__':

    tax_config = {'st_gains': 0.35, 'lt_gains': 0.15, 'federal_tax_rate': 0.22,
                  'state_tax_rate': 0.12}
    money_market_holding = 'VGIT'
    start_date = '1980-01-01'
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
                               start_date=start_date)
    dm.run_multi_component_dual_momentum()




