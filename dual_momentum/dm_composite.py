from dual_momentum.dm_component import DualMomentumComponent
from IPython import embed
from dual_momentum.fred_data import load_fred_data
import numpy as np
import pandas as pd
import hashlib
from pathlib import Path
from dual_momentum.ticker_config import TICKER_CONFIG
from dual_momentum.ticker_data import TickerData
import multiprocessing
import datetime
import time

from dual_momentum.storage import write_to_redis, read_from_redis


class DualMomentumComposite:
    """
    DualMomentumComposite simulates multiple DM components, e.g. reits and equities

    Takes 0.03 seconds

    """

    def __init__(self, parts: list, money_market_holding: str, momentum_leverages: dict,
                 tax_config: dict, start_date: str, leverage: float,
                 borrowing_cost_above_libor: float,
                 force_new_data: bool = False):


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

        self.force_new_data = force_new_data
        self.components = []
        for part in parts:
            if part['weight'] < 0 or part['weight'] > 1:
                raise ValueError(f'Weight for part {part["name"]} has to be between 0 and 1')
            component = DualMomentumComponent(
                name=part['name'], ticker_list=part['ticker_list'], tax_config=tax_config,
                lookback_months=part['lookback_months'], max_holdings=part['max_holdings'],
                use_dual_momentum=part['use_dual_momentum'], start_date=start_date,
                money_market_holding=money_market_holding, weight=part['weight'],
                force_new_data=force_new_data
            )
            self.components.append(component)

        try:
            self.max_lookback_months = max([c.lookback_months for c in self.components if
                                       c.use_dual_momentum])
        # called if only buy and hold components
        except ValueError:
            self.max_lookback_months = 0

        # self.parts = parts
        self.money_market_holding = money_market_holding
        self.momentum_leverages = momentum_leverages
        self.tax_config = tax_config
        self.start_date = start_date
        self.leverage = leverage
        self.borrowing_cost_above_libor = borrowing_cost_above_libor

        self.simulation_finished = False
        self.summary = None

    def __hash__(self) -> str:
        """
        We use hash to create a unique identifier for a configuration. Hence, this uses md5 not
        hash() because it has to be deterministic. ( hash() uses a random seed).

        :return: str
        """
        string_to_hash = (
            f'{[c.__hash__() for c in self.components]}{self.money_market_holding}'
            f'{self.momentum_leverages}{self.tax_config}{self.start_date}{self.leverage}'
            f'{self.borrowing_cost_above_libor}{self.force_new_data}'
        )
        md5 = hashlib.md5(string_to_hash.encode('utf8')).hexdigest()
        return md5

    # @property
    # def file_path(self):
    #     """
    #     filepath for the simulated pickle file
    #
    #     :return:
    #     """
    #
    #     return Path(DATA_PATH, 'dm_composite_data', f'{self.__hash__()}.pickle')

    def preload_data_in_parallel(self):
        """
        Preload all necessary ticker data in parallel

        Loading ticker data one after another is slow--each one takes 1-2 seconds -> by just
        loading all at the beginning as separate processes, we get all the data in 1-2 seconds

        :return:
        """

        tickers_to_init = {'TLT', 'VUSTX', 'VWESX', 'VGIT', 'VFITX', 'FGOVX', 'SPY',
                           'VFINX', self.money_market_holding}

        for component in self.components:
            for ticker in component.ticker_list:

                tickers_to_init.add(ticker)
                while True:
                    early_replacement = TICKER_CONFIG[ticker]['early_replacement']
                    if not early_replacement:
                        break
                    else:
                        ticker = TICKER_CONFIG[ticker]['early_replacement']
                        tickers_to_init.add(ticker)

        if 'ONES' in tickers_to_init: tickers_to_init.remove('ONES')
        mp_results_queue = multiprocessing.Queue()
        for ticker in tickers_to_init:
            multiprocessing.Process(target=self.preload_data_in_parallel_worker,
                                    args=(ticker, mp_results_queue)).start()
        for _ in tickers_to_init:
            mp_results_queue.get()

    @staticmethod
    def preload_data_in_parallel_worker(ticker, mp_results_queue):
        """
        Multiprocessing worker to load data for one ticker from disk or from yahoo

        Puts True into mp_results_queue once it's done fetching

        :param ticker: str
        :param mp_results_queue: multiprocessing.Queue
        :return:
        """
        t = TickerData(ticker=ticker, force_new_data=False)
        t.load_raw_data_or_get_from_yahoo()
        mp_results_queue.put(True)

    def run_multi_component_dual_momentum(self):


        self.df = None
        if not self.force_new_data:
            self.df = read_from_redis(key=self.__hash__())

        # if the simulation was cached in redis, use the cached simulation.
        if self.df is not None:
            self.simulation_finished = True
            return self.df
        else:
            start_time = time.time()
            self.libor = load_fred_data('libor_rate', return_type='dict')


            self.preload_data_in_parallel()
            self.df = TickerData('ONES').data_monthly
            df = self.df
            df.drop(['Adj Close', 'Close'], inplace=True, axis=1)
            df['cash_portion'] = 0.0
            df['performance_pretax'] = 0.0
            df['taxes'] = 0.0

            # each money market holding works like a buy and hold component
            for mm_holding in {'TLT', 'VGIT', 'SPY', self.money_market_holding}:
                component = DualMomentumComponent(
                    name=f'__{mm_holding}', ticker_list=[mm_holding], tax_config=self.tax_config,
                    lookback_months=12, max_holdings=1, use_dual_momentum=False, start_date=self.start_date,
                    money_market_holding=mm_holding, force_new_data=self.force_new_data
                )
                component.run_dual_momentum()

                df[f'__{mm_holding}_performance_pretax'] = component.df['performance_pretax']
                df[f'__{mm_holding}_performance_posttax'] = component.df['performance_posttax']
                df[f'__{mm_holding}_taxes'] = component.df['taxes']

            for idx, component in enumerate(self.components):
                component.run_dual_momentum()

                if idx == 0:
                    df['tbil_performance_pretax'] = component.df['tbil_performance_pretax']

                df[f'{component.name}_holding'] = component.df['holding']
                df[f'{component.name}_performance_pretax'] = component.df['performance_pretax']
                df[f'{component.name}_taxes'] = component.df['taxes']
                df[f'{component.name}_performance_posttax'] = component.df['performance_posttax']

                df['performance_pretax'] += component.weight * component.df['performance_pretax']
                df['taxes'] += component.weight * component.df['taxes']
                df['cash_portion'] += component.weight * component.df['cash_portion']

            df['leverage'] = 0.0
            df['mmh'] = self.money_market_holding
            df['leverage_costs'] = 0
            df['lev_performance_pretax'] = 1.0
            df['taxes_month'] = 0.0
            df['taxes_due_total'] = 0.0
            df['taxes_paid'] = 0.0
            df['lev_performance_posttax'] = 10000
            df['lev_dd'] = 0.0

            # pandas dataframes are slow with df.iterrows. It's much faster to turn the df into
            # a dict and then pick values from it
            df_as_dict = df.to_dict('index')
            df_indexes = list(df.index)

            for idx, date in enumerate(df_indexes):
                if idx < self.max_lookback_months:
                    continue

                row = df_as_dict[date]
                year, month = date

                # prev_total = df.at[df.index[idx - 1], 'lev_performance_posttax']
                prev_total = df_as_dict[df_indexes[idx-1]]['lev_performance_posttax']

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
                        mm_pretax = row[f'__{self.money_market_holding}_performance_pretax'] - 1
                        lev_performance_pretax += percentage_cash * mm_pretax
                        taxes_month += row[f'__{self.money_market_holding}_taxes'] * \
                                       percentage_cash * prev_total
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

                    df_as_dict[date]['leverage_cost'] = leverage_cost
                    lev_performance_pretax -= leverage_cost

                # taxes_due_total = taxes_month + df.at[df.index[idx - 1], 'taxes_due_total']
                taxes_due_total = taxes_month + df_as_dict[df_indexes[idx - 1]]['taxes_due_total']
                taxes_paid = 0

                # calculate returns after taxes
                lev_performance_posttax = lev_performance_pretax * prev_total
                # if end of january (200x, 12), pay taxes
                if month == 12 and taxes_due_total > 0:
                    lev_performance_posttax -= taxes_due_total
                    taxes_paid = taxes_due_total
                    taxes_due_total = 0

                df_as_dict[date]['lev_performance_pretax'] = lev_performance_pretax
                df_as_dict[date]['taxes_month'] = taxes_month
                df_as_dict[date]['taxes_due_total'] = taxes_due_total
                df_as_dict[date]['taxes_paid'] = taxes_paid
                df_as_dict[date]['lev_performance_posttax'] = lev_performance_posttax
                df_as_dict[date]['leverage'] = self.leverage
                df_as_dict[date]['cash_portion'] = max(0, percentage_cash)

            self.df = pd.DataFrame.from_dict(df_as_dict, orient='index')

            write_to_redis(key=self.__hash__(), value = self.df, expiration=3600)
            print(f"running dual momentum on composite took {time.time() - start_time}.")

        self.simulation_finished = True
        return self.df

    def generate_results_summary(self):


        self.summary = read_from_redis(f'summary_{self.__hash__()}')
        if self.summary:
            return

        summary = {}

        self.df['performance_strategy_pretax'] = self.df['lev_performance_pretax']
        self.df['performance_strategy_posttax'] = self.df['lev_performance_posttax'].pct_change(
                                                            ).fillna(0) + 1
        self.df['performance_sp500_pretax'] = self.df['__SPY_performance_pretax']
        self.df['performance_sp500_posttax'] = self.df['__SPY_performance_posttax']

        for name in ['strategy', 'sp500']:
            for tax_type in ['pretax', 'posttax']:
                self.df[f'performance_{name}_{tax_type}_cumulative'] = np.cumprod(self.df[
                                                              f'performance_{name}_{tax_type}'])

                dd_arr, max_dd, max_dd_date = self.generate_drawdown_data(self.df[
                                                f'performance_{name}_{tax_type}_cumulative'])
                self.df[f'drawdown_{name}_{tax_type}'] = dd_arr
                summary[f'max_dd_{name}_{tax_type}'] = max_dd
                summary[f'max_dd_{name}_{tax_type}_str'] = f'{round((1 - max_dd) * 100, 2)}%'
                summary[f'max_dd_date_{name}_{tax_type}'] = max_dd_date
                summary[f'max_dd_date_{name}_{tax_type}_str'] = datetime.datetime(
                    max_dd_date[0], max_dd_date[1], 1).strftime("%b %Y")

                returns = self.df[f'performance_{name}_{tax_type}_cumulative'][-1] - 1
                summary[f'total_returns_{name}_{tax_type}'] = returns
                cagr = returns ** (1 / ((len(self.df) - self.max_lookback_months) / 12))
                summary[f'cagr_{name}_{tax_type}'] = cagr
                summary[f'cagr_{name}_{tax_type}_str'] = f'{round((cagr - 1) * 100, 2)}%'


            return_minus_riskfree = (self.df[f'performance_{name}_pretax'] -
                             self.df['tbil_performance_pretax'])[self.max_lookback_months: -1]
            summary[f'sharpe_{name}'] = np.sqrt(12) * return_minus_riskfree.mean() / \
                                        return_minus_riskfree.std()

            downside_dev = return_minus_riskfree.copy()
            downside_dev[downside_dev > 0] = 0
            downside_dev = np.sqrt(np.mean(downside_dev ** 2)) * np.sqrt(12)
            summary[f'sortino_{name}'] = np.mean(return_minus_riskfree) / downside_dev * 12

            # alpha = 2
            ann_vol = return_minus_riskfree.std() * (12 ** 0.5)
            summary[f'annual_volatility_{name}'] = ann_vol
            summary[f'annual_volatility_{name}_str'] = f'{round(ann_vol * 100, 2)}%'

        # get correlations
        summary['correlations'] = self.get_correlation_summary_data()

        # get monthly holdings and return data
        summary['monthly_data'] = self.get_monthly_returns_summaries()

        for key, val in summary.items():
            if isinstance(val, float):
                summary[key] = round(val, 4)
        self.summary = summary

        write_to_redis(key=f'summary_{self.__hash__()}', value=summary, expiration=3600)


    @staticmethod
    def generate_drawdown_data(cumulative_series: pd.Series):
        """
        Calculate monthly drawdowns in %

        :param cumulative_series:
        :return:
        """

        perf_arr = np.array(cumulative_series)
        index_arr = np.array(cumulative_series.index)
        dd_arr = np.zeros(len(cumulative_series), dtype=float)
        max_dd = 1.0
        max_dd_date = None
        for i in range(1, (len(perf_arr))):
            max_performance_so_far = np.max(perf_arr[0:i])

            dd = min(1.0, 1.0 * perf_arr[i] / max_performance_so_far)
            dd_arr[i] = dd
            if dd < max_dd:
                max_dd = dd
                max_dd_date = index_arr[i]

        return dd_arr, max_dd, max_dd_date

    def get_correlation_summary_data(self):
        """
        Get data on correlation between strategy, S&P 500, and the dm components
        Returns data preformatted for MDB Table

        :return: dict
        """

        columns_to_names = {f'{component.name}_performance_pretax': component.name for
                            component in self.components}
        columns_to_names['performance_strategy_pretax'] = 'Strategy'
        columns_to_names['performance_sp500_pretax'] = 'S&P 500'
        correlation_columns = [
            {'label': '', 'field': 'comparison'},
            {'label': 'Strategy', 'field': 'performance_strategy_pretax'},
            {'label': 'S&P 500', 'field': 'performance_sp500_pretax'}
        ]
        correlation_columns += [
            {'label': component.name, 'field': f'{component.name}_performance_pretax'} for
            component in self.components
        ]

        correlations = self.df[[col['field'] for col in correlation_columns[1:]]].corr()
        correlation_data = []
        for _, row in correlations.iterrows():
            # for some reason, MDB tables requires each row to be a dict. Which would be fine if
            # it actuall used the field specified in the columns to figure out what value to
            # display. However, instead, it just displays the value entered first at the begining,
            # followed by the second one and so on, so they need to be added !in order! to an
            # !unordered object! Never tell the methods...
            row_data = {'comparison': columns_to_names[row.name]}
            row_data.update({comp: round(row[comp], 4) for comp in row.index})
            correlation_data.append(row_data)

        return {
            'columns': correlation_columns,
            'data': correlation_data
        }

    def get_monthly_returns_summaries(self):
        """
        Returns data on components and holdings month by month

        :return:
        """

        monthly_data = []

        self.df['prev_total_pretax'] = self.df.performance_strategy_pretax_cumulative.shift(
            1).fillna(1)
        self.df['prev_total_posttax'] = self.df.performance_strategy_posttax_cumulative.shift(
            1).fillna(1)
        df_as_dict = self.df.to_dict('index')
        # df_indexes = list(df.index)

        for idx, date in enumerate(self.df.index):
            if idx < self.max_lookback_months:
                continue
            if idx == len(df_as_dict) - 1:
                continue
            row = df_as_dict[date]

            return_mmh_pretax = round(row[f'__{row["mmh"]}_performance_pretax'], 4)
            return_mmh_posttax = round(row[f'__{row["mmh"]}_performance_posttax'], 4)

            holdings = []
            for name in [component.name for component in self.components]:

                holding = {'name': name}
                tickers = row[f'{name}_holding']

                return_tickers_pretax = round(row[f'{name}_performance_pretax'], 4)
                return_tickers_posttax = round(row[f'{name}_performance_posttax'], 4)


                # 100% cash -> only list MMH holding and returns
                if tickers == ['CASH']:
                    holding['holdings'] = [row['mmh']]
                    holding['pretax'] = return_mmh_pretax
                    holding['posttax'] = return_mmh_posttax

                # 50% cash -> returns 50% from tickers and 50% from mmh
                elif len(tickers) == 2 and tickers[1] == 'CASH':
                    holding['holdings'] = tickers
                    holding['pretax'] = return_tickers_pretax / 2 + return_mmh_pretax / 2
                    holding['posttax'] = return_tickers_posttax / 2 + return_mmh_posttax / 2

                else:
                    holding['holdings'] = tickers
                    holding['pretax'] = return_tickers_pretax
                    holding['posttax'] = return_tickers_posttax

                holdings.append(holding)

            monthly_data.append({
                'date': date,
                'date_str': datetime.datetime(date[0], date[1], 1).strftime("%b %Y"),
                'holdings': holdings,
                'value_start_pretax': row['prev_total_pretax'],
                'value_start_posttax': row['prev_total_posttax'],
                'value_end_pretax': row['performance_strategy_pretax_cumulative'],
                'value_end_posttax': row['performance_strategy_posttax_cumulative'],
                'value_end_spy_pretax': round(row['performance_sp500_pretax_cumulative'], 4),
                'value_end_spy_posttax': round(row['performance_sp500_posttax_cumulative'], 4)
            })

        return monthly_data


if __name__ == '__main__':
    # fed_st_gains: float, fed_lt_gains: float, state_st_gains: float,
    # state_lt_gains: float):
    tax_config = {'fed_st_gains': 0.22, 'fed_lt_gains': 0.15, 'state_st_gains': 0.12,
                  'state_lt_gains': 0.051}
    # tax_config = {'st_gains': 0.0, 'lt_gains': 0.0, 'federal_tax_rate': 0.0,
    #               'state_tax_rate': 0.0}
    money_market_holding = 'VGIT'
    start_date = '1980-01-01'
    leverage = 1
    borrowing_cost_above_libor = 1.5
    parts = [
        {
            'name': 'equities',
            'ticker_list': ['VTI', 'QQQ', 'IEMG', 'IEFA'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings':2, 'weight': 0.5
        },
        {
            'name': 'reits',
            'ticker_list': ['VNQ', 'VNQI', 'REM'],
            'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 1, 'weight': 0.5
        }
    ]

    momentum_leverages = {
       'months_for_lev': 3,
                    0.80: -0.3, 0.85: -0.3, 0.90: -0.2, 0.95: -0.2,
        1.30:  0.2, 1.20:  0.1, 1.15:  0.1, 1.10:  0.0, 1.05:  0.0
    }

    import time
    s = time.time()

    dm = DualMomentumComposite(parts=parts, money_market_holding=money_market_holding,
                               momentum_leverages=momentum_leverages, tax_config=tax_config,
                               start_date=start_date,
                               leverage=leverage,
                               borrowing_cost_above_libor=borrowing_cost_above_libor,
                               force_new_data=False)

    dm.run_multi_component_dual_momentum()
    dm.generate_results_summary()


    print(time.time() - s )

    embed()


