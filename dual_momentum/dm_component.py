from dual_momentum.rates import load_tbill_rates, get_tax_rates_by_category, get_tax_rates_by_ticker
from dual_momentum.fred_data import load_fred_data
from dual_momentum.ticker_data import TickerData
import re
import numpy as np
import pandas as pd
from pathlib import Path
from dual_momentum.dm_config import DATA_PATH
from dual_momentum.utilities import file_exists_and_less_than_1hr_old

import hashlib

from IPython import embed


class DualMomentumComponent:
    """
    DualMomentumComponent simulates one DM component, e.g. equities or REITs

    >>> ticker_list = [{'ticker': 'VTI', 'tax_category': 'equities'}]
    >>> tax_config = {'st_gains': 0.35, 'lt_gains': 0.15, 'federal_tax_rate': 0.22,
    ...               'state_tax_rate': 0.12}
    >>> dmc = DualMomentumComponent(name='equities', ticker_list=ticker_list, lookback_months=12,
    ...                             max_holdings=1, start_date='1980-01-01', use_dual_momentum=True,
    ...                             money_market_holding='VGIT', tax_config=tax_config)

    """

    def __init__(self, name: str, ticker_list: list, lookback_months: int, max_holdings: int,
               start_date: str, use_dual_momentum: bool, money_market_holding: str,
               tax_config: dict,
               force_new_data: bool = False, use_early_replacements: bool = True,
               day_of_month_for_monthly_data: int = -1,
                 weight = None,
               ):

        if not use_dual_momentum and len(ticker_list) > 1:
            raise ValueError(f"Buy and hold can only be chosen with one single ticker but not "
                             f"{ticker_list}.")

        if not isinstance(name, str):
            raise ValueError(f'name has to be string, not {type(name)} ({name}.')
        if not isinstance(ticker_list, list):
            raise ValueError(f'ticker_list has to be list, not {type(ticker_list)}.')
        if not isinstance(lookback_months, int):
            raise ValueError(f'lookback_months has to be int, not {type(lookback_months)}.')
        if max_holdings not in [1,2]:
            raise ValueError(f'max_holdings has to be 1 or 2 but not {max_holdings}')
        if not re.match(r'[\d]{4}-[\d]{2}-[\d]{2}', start_date):
            raise ValueError(f'start_date has to be in the format "YYYY-MM-DD", not {start_date}.')
        if not isinstance(money_market_holding, str):
            raise ValueError(f'money_market_holding has to be str, not '
                             f'{type(money_market_holding)}')

        if not (weight is None or 0 <= weight <= 1):
            raise ValueError(f'weight has to be None or value between 0 and 1, not {weight}.')

        self.name = name
        self.ticker_list = ticker_list
        self.lookback_months = lookback_months
        self.start_date = start_date
        self.use_dual_momentum = use_dual_momentum
        self.money_market_holding = money_market_holding

        # optional component, placed here so we don't need both the config and the component
        # in dm_composite
        self.weight = weight
        self.tax_config = tax_config

        self.tax_rates_by_category = get_tax_rates_by_category(
            fed_st_gains=tax_config['fed_st_gains'], fed_lt_gains=tax_config['fed_lt_gains'],
            state_st_gains=tax_config['state_st_gains'], state_lt_gains=tax_config[
                'state_lt_gains'])
            # st_gains=tax_config['st_gains'],
            #     lt_gains=tax_config['lt_gains'], federal_tax_rate=tax_config['federal_tax_rate'],
            #     state_tax_rate=tax_config['state_tax_rate'])
        self.tax_rates_by_ticker = get_tax_rates_by_ticker(self.tax_rates_by_category,
                                               self.ticker_list + [money_market_holding, 'TBIL'])

        # if ticker is a dict like {'ticker': 'VTI', 'tax_category': 'equities'}
        self.ticker_list = []
        for ticker in ticker_list:
            if isinstance(ticker, dict):
                self.ticker_list.append(ticker['ticker'])
            elif isinstance(ticker, str):
                self.ticker_list.append(ticker)


        self.max_holdings = max_holdings
        if len(self.ticker_list) == 1:
            self.max_holdings = 1

        # tickerdata config
        self.force_new_data = force_new_data
        self.use_early_replacements = use_early_replacements
        self.day_of_month_for_monthly_data = day_of_month_for_monthly_data
        self.df = None


    def __hash__(self) -> str:
        """
        We use hash to create a unique identifier for a configuration. Hence, this uses md5 not
        hash() because it has to be deterministic. ( hash() uses a random seed).

        :return: str
        """

        string_to_hash = (f'{self.name}{self.ticker_list}{self.lookback_months}{self.max_holdings}'
                    f'{self.start_date}{self.use_dual_momentum}{self.money_market_holding}'
                    f'{self.force_new_data}{self.use_early_replacements}{self.weight}'
                    f'{self.day_of_month_for_monthly_data}{self.tax_config}')
        md5 = hashlib.md5(string_to_hash.encode('utf8')).hexdigest()
        return md5


    @property
    def file_path(self):
        """
        filepath for the simulated pickle file

        :return:
        """

        return Path(DATA_PATH, 'dm_component_data', f'{self.__hash__()}.pickle')

    # @profile
    def run_dual_momentum(self):
        """
        Runs a dual-momentum backtest
        Tries to load from disk first, then simulates

        :return:
        """

        if not self.force_new_data and file_exists_and_less_than_1hr_old(self.file_path):
            print("using cached dm component data", self.__hash__())
            self.df = pd.read_pickle(self.file_path)
        # if False: pass
        else:
            # initialize df with tbil rates
            tbil_df = load_fred_data('tbil_rate', return_type='df')
            self.df = TickerData('ONES').data_monthly
            self.df.drop(['Close', 'Adj Close'], inplace=True, axis=1)
            self.df['tbil_rate'] = tbil_df['index']
            self.df['tbil_rate'] += 100
            self.df['tbil_performance_pretax'] = (self.df['tbil_rate'] / 100) ** (1 / 12)

            # we're calculating momentum after taxes, so tbils should be compared on a posttax
            # basis. I don't have data on tbil cap gains bet it seems reasonable to assume that
            # they are close to 0.
            self.df['tbil_performance_posttax'] = 1 + \
                (self.df['tbil_performance_pretax'] - 1) * \
                (1 - self.tax_rates_by_ticker['TBIL']['INCOME'])
            self.df['holding'] = ''
            self.df['cap_gains'] = 0.0
            self.df['div_gains'] = 0.0

            self.df['performance_pretax'] = 1.0
            self.df['taxes'] = 0.0
            self.df['performance_posttax'] = 1.0
            self.df['cash_portion'] = 0.0

            if self.money_market_holding != 'TBIL':
                self.add_ticker_to_df(self.money_market_holding)

            for ticker in self.ticker_list:
                self.add_ticker_to_df(ticker)

            # store df as dict for better performance on row-based tasks
            self.df_as_dict = self.df.to_dict('index')
            self.df_indexes = list(self.df.index)

            # identify the holdings for each month
            self.identify_holdings_by_month()

            # calculate the returns based on the holdings
            self.calculate_returns_based_on_holdings()

            # finally turn the dict back into a df
            self.df = pd.DataFrame.from_dict(self.df_as_dict, orient='index')
            self.df.to_pickle(self.file_path)

        return self.df


    def identify_holdings_by_month(self):
        """
        For each month, finds and stores the tickers with the best momentum.
        If buy and hold -> only store that one ticker
        if low momentum -> 1 or both holdings are CASH
        else: tow tickers
        """

        # pandas dataframes are slow with df.iterrows. It's much faster to turn the df into
        # a dict and then pick values from it

        for idx, date in enumerate(self.df_indexes):
            row = self.df_as_dict[date]

            count_active_tickers = 0
            momentums = {}

            # figure out current momentum for each ticker
            for ticker in self.ticker_list:

                # # figure out if we should use long term (held 1+ year) or short term momentum
                # months_held = self.determine_holding_period(ticker, idx)
                # if months_held >= 12:
                #     ticker_mom = row[f'{ticker}_lt_mom']
                # else:
                #     ticker_mom = row[f'{ticker}_st_mom']

                ticker_mom = row[f'{ticker}_pretax_mom']


                # adjusted for duration, e.g. bonds held for 6 months ->
                # with 5% tbil rate, would have returned 2.5%
                if ticker_mom > ((row['tbil_performance_pretax'] - 1) *
                                 self.lookback_months / 12 + 1):
                    momentums[ticker] = ticker_mom

            if not self.use_dual_momentum:
                self.df_as_dict[date]['holding'] = self.ticker_list
            elif len(momentums) == 0:
                self.df_as_dict[date]['holding'] = ['CASH']
            elif len(momentums) == 1:
                if self.max_holdings == 1:
                    self.df_as_dict[date]['holding'] = [list(momentums)[0]]
                else:
                    self.df_as_dict[date]['holding'] = [list(momentums)[0], 'CASH']
            else:
                sorted_moms = sorted(momentums.items(), key=lambda x: x[1], reverse=True)
                if self.max_holdings == 1:
                    self.df_as_dict[date]['holding'] = [sorted_moms[0][0]]
                else:
                    self.df_as_dict[date]['holding'] = [sorted_moms[0][0], sorted_moms[1][0]]

    def calculate_returns_based_on_holdings(self):
        """
        Calculate the monthly returns based on the holdings

        :return:
        """

        for idx, date in enumerate(self.df_indexes):
            row = self.df_as_dict[date]


            # when in cash, no gains or losses (money market holding gets accounted for with
            # leverage
            if row['holding'] == ['CASH']:
                self.df_as_dict[date]['cash_portion'] = 1.0
                self.df_as_dict[date]['performance_posttax'] = 1.0
                # self.df.at[date, 'cash_portion'] = 1.0
                # self.df.at[date, 'performance_posttax'] = 1.0
                continue

            holding1 = row['holding'][0]
            if len(row['holding']) > 1:
                holding2 = row['holding'][1]
            else:
                holding2 = None

            if holding2 and holding2 == 'CASH':
                self.df_as_dict[date]['cash_portion'] = 0.5
                # self.df.at[date, 'cash_portion'] = 0.5

            # break at last row (we don't know the returns yet)
            if idx + 1 == len(self.df_as_dict):
                break

            # process holding 1
            next_month_date = self.df_indexes[idx+1]

            h1_next_month_close = self.df_as_dict[next_month_date][f'{holding1}_close']
            # h1_next_month_close = self.df.at[next_month_date, f'{holding1}_close']
            h1_next_month_adj_close = self.df_as_dict[next_month_date][f'{holding1}_adj_close']
            # h1_next_month_adj_close = self.df.at[next_month_date, f'{holding1}_adj_close']


            cap_gains = h1_next_month_close / row[f'{holding1}_close'] - 1
            total_gains = h1_next_month_adj_close / row[f'{holding1}_adj_close'] - 1
            div_gains = total_gains - cap_gains

            h1_months_held = self.determine_holding_period(holding1, idx)
            if h1_months_held >= 12:
                taxes = cap_gains * self.tax_rates_by_ticker[holding1]['LT_GAINS']
            else:
                taxes = cap_gains * self.tax_rates_by_ticker[holding1]['ST_GAINS']
            taxes += div_gains * self.tax_rates_by_ticker[holding1]['INCOME']

            if holding2:
                if holding2 == 'CASH':
                    div_gains = div_gains * 0.5     # div_gains are just div_gains from h1
                    cap_gains = cap_gains * 0.5     # now, we're holding 50% cash -> only 50% gains
                    taxes = taxes * 0.5
                    self.df_as_dict[date]['cash_portion'] = 0.5
                    # self.df.at[date, 'cash_portion'] = 0.5

                else:
                    # h2_next_month_close = self.df.at[next_month_date, f'{holding2}_close']
                    h2_next_month_close = self.df_as_dict[next_month_date][f'{holding2}_close']
                    # h2_next_month_adj_close = self.df.at[next_month_date,
                    #                                      f'{holding2}_adj_close']
                    h2_next_month_adj_close = self.df_as_dict[next_month_date][
                                                              f'{holding2}_adj_close']
                    h2_cap_gains = h2_next_month_close / row[f'{holding2}_close'] - 1
                    h2_total_gains = h2_next_month_adj_close / row[f'{holding2}_adj_close'] - 1
                    h2_div_gains = h2_total_gains - h2_cap_gains

                    h2_months_held = self.determine_holding_period(holding2, idx)
                    if h2_months_held >= 12:
                        h2_taxes = h2_cap_gains * self.tax_rates_by_ticker[holding2]['LT_GAINS']
                    else:
                        h2_taxes = h2_cap_gains * self.tax_rates_by_ticker[holding2]['ST_GAINS']

                    h2_taxes += h2_div_gains * self.tax_rates_by_ticker[holding2]['INCOME']

                    # with 2 non-cash holdings, gains and taxes are averaged.
                    div_gains = div_gains * 0.5 + h2_div_gains * 0.5
                    cap_gains = cap_gains * 0.5 + h2_cap_gains * 0.5
                    taxes = taxes * 0.5 + h2_taxes * 0.5

            # finally, add the data to the dataframe
            # self.df.at[date, 'div_gains'] = div_gains
            # self.df.at[date, 'cap_gains'] = cap_gains
            # self.df.at[date, 'taxes'] = taxes
            # self.df.at[date, 'performance_pretax'] = cap_gains + div_gains + 1
            # self.df.at[date, 'performance_posttax'] = cap_gains + div_gains - taxes + 1
            self.df_as_dict[date]['div_gains'] = div_gains
            self.df_as_dict[date]['cap_gains'] = cap_gains
            self.df_as_dict[date]['taxes'] = taxes
            self.df_as_dict[date]['performance_pretax'] = cap_gains + div_gains + 1
            self.df_as_dict[date]['performance_posttax'] = cap_gains + div_gains - taxes + 1

    def add_ticker_to_df(self, ticker):
        """
        Adds a ticker to the dataframe
        :param ticker: str
        :return:
        """

        new_stock = TickerData(ticker=ticker, use_early_replacements=self.use_early_replacements,
                               day_of_month_for_monthly_data=self.day_of_month_for_monthly_data,
                               force_new_data=self.force_new_data,
                               ).data_monthly

        new_stock['cap_gains'] = new_stock['Close'].shift(-1) / new_stock['Close']
        new_stock['total_gains'] = new_stock['Adj Close'].shift(-1) / new_stock['Adj Close']
        new_stock['div_gains'] = new_stock['total_gains'] - new_stock['cap_gains'] + 1

        # capital gains, total gains, dividend gains during duration.
        new_stock['cap_dur'] = new_stock['Close'] / new_stock['Close'].shift(self.lookback_months)
        new_stock['total_dur'] = (new_stock['Adj Close'] /
                                     new_stock['Adj Close'].shift(self.lookback_months))
        new_stock['div_dur'] = new_stock['total_dur'] - new_stock['cap_dur']

        st = 1 - self.tax_rates_by_ticker[ticker]['ST_GAINS']
        lt = 1 - self.tax_rates_by_ticker[ticker]['LT_GAINS']
        div = 1 - self.tax_rates_by_ticker[ticker]['INCOME']

        # ST momentum = capital gains + dividends. Tax cap gains only if greater than 1
        new_stock['st_mom'] = np.where(new_stock['cap_dur'] <= 1.0,
                                       new_stock['cap_dur'],
                                       (new_stock['cap_dur'] - 1) * st + 1)
        new_stock['st_mom'] += new_stock['div_dur'] * div
        new_stock['lt_mom'] = np.where(new_stock['cap_dur'] <= 1.0,
                                       new_stock['cap_dur'],
                                       (new_stock['cap_dur'] - 1) * lt + 1)
        new_stock['lt_mom'] += new_stock['div_dur'] * div

        # add to main df for component
        self.df[f'{ticker}_adj_close'] = new_stock['Adj Close']
        self.df[f'{ticker}_close'] = new_stock['Close']
        self.df[f'{ticker}_st_mom'] = new_stock['st_mom']
        self.df[f'{ticker}_lt_mom'] = new_stock['lt_mom']
        self.df[f'{ticker}_pretax_mom'] = new_stock['total_dur']

    def determine_holding_period(self, ticker: str, idx : int) -> int:
        """
        Determines the holding period for a ticker

        Shortcut: stop at 12. We only care about long term vs short term for this function

        :param ticker:
        :param df_as_dict: a dataframe parsed to a list of dicts
        :param df_indexes: a sorted list of dataframe indexes, eg [(1990, 1), (1990, 2)...]
        :param idx: int
        :return:
        """

        months_held_before = 0
        while True:
            if months_held_before >= 12 or idx - 1 - months_held_before < 0:
                break

            prev_date = self.df_indexes[idx - 1 - months_held_before]
            prev_holdings = self.df_as_dict[prev_date]['holding']

            if ticker not in prev_holdings:
                break
            else:
                months_held_before += 1

        return months_held_before


    # @staticmethod
    # def determine_holding_period(ticker: str, holdings_arr: np.array, idx: int):
    #     """
    #     Determines the holding period for a ticker
    #
    #     Shortcut: stop at 12. We only care about long term vs short term for this function
    #
    #     :param ticker:
    #     :param holdings_arr:
    #     :param idx: current month (expressed as an int)
    #     :return:
    #     """
    #
    #     months_held_before = 0
    #
    #     while True:
    #         # break if held at least 12 months or we're trying to access a negative idx at the
    #         # beginning of the list
    #
    #         if months_held_before >= 12 or idx - 1 - months_held_before < 0:
    #             return months_held_before
    #         # if :
    #         #     return months_held_before
    #         prev_holdings = holdings_arr[idx - 1 - months_held_before]
    #         if ticker not in prev_holdings:
    #             break
    #         else:
    #             months_held_before += 1
    #
    #     return months_held_before

if __name__ == '__main__':
    ticker_list = ['VNQ', 'VNQI', 'IEF']
    tax_config = {'st_gains': 0.7, 'lt_gains': 0.7, 'federal_tax_rate': 0.7,
                   'state_tax_rate': 0.7}
    tax_config = {'st_gains': 0.0, 'lt_gains': 0.00, 'federal_tax_rate': 0.00,
                   'state_tax_rate': 0.00}
    dmc = DualMomentumComponent(name='equities', ticker_list=ticker_list, lookback_months=12,
                                max_holdings=2, start_date='1980-01-01', use_dual_momentum=True,
                                money_market_holding='VGIT', tax_config=tax_config)

    dmc.run_dual_momentum()

    dmc.df['performance_pretax_cumulative'] = np.cumprod(dmc.df['performance_pretax'])
    dmc.df['performance_posttax_cumulative'] = np.cumprod(dmc.df['performance_posttax'])

    print(dmc.df['performance_posttax_cumulative'][-2], dmc.df['performance_pretax_cumulative'][-2])

