from rates import load_tbill_rates, get_tax_rates_by_category, get_tax_rates_by_ticker
from ticker_data import TickerData
import re
import numpy as np


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

        self.name = name
        self.ticker_list = ticker_list
        self.looback_months = lookback_months
        self.max_holdings = max_holdings
        self.start_date = start_date
        self.use_dual_momentum = use_dual_momentum
        self.money_market_holding = money_market_holding

        self.tax_rates_by_category = get_tax_rates_by_category(st_gains=tax_config['st_gains'],
                lt_gains=tax_config['lt_gains'], federal_tax_rate=tax_config['federal_tax_rate'],
                state_tax_rate=tax_config['state_tax_rate'])
        self.tax_rates_by_ticker = get_tax_rates_by_ticker(self.tax_rates_by_category,
                                                       self.ticker_list + [money_market_holding])

        # if ticker is a dict like {'ticker': 'VTI', 'tax_category': 'equities'}
        self.ticker_list = []
        for ticker in ticker_list:
            if isinstance(ticker, dict):
                self.ticker_list.append(ticker['ticker'])
            elif isinstance(ticker, str):
                self.ticker_list.append(ticker)

        # tickerdata config
        self.force_new_data = force_new_data
        self.use_early_replacements = use_early_replacements
        self.day_of_month_for_monthly_data = day_of_month_for_monthly_data

        # load tbil rates into initial df as they will be needed in every case.
        self.df = load_tbill_rates()

    def run_dual_momentum(self):
        """
        Runs a dual-momentum backtest

        :return:
        """

        self.df['holding'] = ''         # holdings
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

        # identify the holdings for each month
        self.identify_holdings_by_month()

        # calculate the returns based on the holdings
        self.calculate_returns_based_on_holdings()

        return self.df


    def identify_holdings_by_month(self):
        """
        For each month, finds and stores the tickers with the best momentum.
        If buy and hold -> only store that one ticker
        if low momentum -> 1 or both holdings are CASH
        else: tow tickers
        """

        for idx, r in enumerate(self.df.iterrows()):
            date, row = r

            count_active_tickers = 0
            momentums = {}

            holdings_arr = np.array(self.df['holding']) # for quick access via idx

            # figure out current momentum for each ticker
            for ticker in self.ticker_list:

                # figure out if we should use long term (held 1+ year) or short term momentum
                months_held = self.determine_holding_period(ticker, holdings_arr, idx)
                if months_held > 11:
                    ticker_mom = row[f'{ticker}_lt_mom']
                else:
                    ticker_mom = row[f'{ticker}_st_mom']

                # adjusted for duration, e.g. bonds held for 6 months ->
                # with 5% tbil rate, would have returned 2.5%
                if ticker_mom > ((row['tbil_rate'] / 100 - 1) * self.looback_months / 12 + 1):
                    momentums[ticker] = ticker_mom

            if not self.use_dual_momentum:
                self.df.at[date, 'holding'] = self.ticker_list  # list of one ticker
            elif len(momentums) == 0:
                self.df.at[date, 'holding'] = ['CASH']
            elif len(momentums) == 1:
                if self.max_holdings == 1:
                    self.df.at[date, 'holding'] = [list(momentums)[0]]
                else:
                    self.df.at[date, 'holding'] = [list(momentums)[0], 'CASH']
            else:
                sorted_moms = sorted(momentums.items(), key=lambda x: x[1], reverse=True)
                if self.max_holdings == 1:
                    self.df.at[date, 'holding'] = [sorted_moms[0][0]]
                else:
                    self.df.at[date, 'holding'] = [sorted_moms[0][0], sorted_moms[1][0]]


    def calculate_returns_based_on_holdings(self):
        """
        Calculate the monthly returns based on the holdings

        :return:
        """

        # Now that we know the holdings, calculate the actual returns
        holdings = np.array(self.df['holding'])
        for idx, r in enumerate(self.df.iterrows()):
            date, row = r
            print(idx, date)

            # when in cash, no gains or losses (money market holding gets accounted for with
            # leverage
            if row['holding'] == ['CASH']:
                self.df.at[date, 'cash_portion'] = 1.0
                self.df.at[date, 'performance_posttax'] = 1.0
                continue

            holding1 = row['holding'][0]
            if len(row['holding']) > 1:
                holding2 = row['holding'][1]
            else:
                holding2 = None

            if holding2 and holding2 == 'CASH':
                self.df.at[date, 'cash_portion'] = 0.5

            # break at last row (we don't know the returns yet)
            if idx + 1 == len(self.df):
                break

            # process holding 1
            h1_next_month_close = self.df.at[self.df.index[idx + 1], f'{holding1}_close']
            h1_next_month_adj_close = self.df.at[self.df.index[idx + 1], f'{holding1}_adj_close']
            cap_gains = h1_next_month_close / row[f'{holding1}_close'] - 1
            total_gains = h1_next_month_adj_close / row[f'{holding1}_adj_close'] - 1
            div_gains = total_gains - cap_gains

            h1_months_held = self.determine_holding_period(holding1, holdings, idx)
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
                    self.df.at[date, 'cash_portion'] = 0.5

                else:
                    h2_next_month_close = self.df.at[self.df.index[idx + 1], f'{holding2}_close']
                    h2_next_month_adj_close = self.df.at[self.df.index[idx + 1],
                                                         f'{holding2}_adj_close']
                    h2_cap_gains = h2_next_month_close / row[f'{holding2}_close'] - 1
                    h2_total_gains = h2_next_month_adj_close / row[f'{holding2}_adj_close'] - 1
                    h2_div_gains = h2_total_gains - h2_cap_gains

                    h2_months_held = self.determine_holding_period(holding2, holdings, idx)
                    if h2_months_held >= 12:
                        h2_taxes = h2_cap_gains * self.tax_rates_by_ticker[holding2]['LT_GAINS']
                    else:
                        h2_taxes = h2_cap_gains * self.tax_rates_by_ticker[holding2]['ST_GAINS']
                    h2_taxes += h2_div_gains * self.tax_rates_by_ticker[holding2]['DIVS']

                    # with 2 non-cash holdings, gains and taxes are averaged.
                    div_gains = div_gains * 0.5 + h2_div_gains * 0.5
                    cap_gains = cap_gains * 0.5 + h2_cap_gains * 0.5
                    taxes = taxes * 0.5 + h2_taxes * 0.5

            # finally, add the data to the dataframe
            self.df.at[date, 'div_gains'] = div_gains
            self.df.at[date, 'cap_gains'] = cap_gains
            self.df.at[date, 'taxes'] = taxes
            self.df.at[date, 'performance_pretax'] = cap_gains + div_gains + 1
            self.df.at[date, 'performance_posttax'] = cap_gains + div_gains - taxes + 1

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
        new_stock['cap_dur'] = new_stock['Close'] / new_stock['Close'].shift(self.looback_months)
        new_stock['total_dur'] = (new_stock['Adj Close'] /
                                     new_stock['Adj Close'].shift(self.looback_months))
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

    @staticmethod
    def determine_holding_period(ticker: str, holdings_arr: np.array, idx: int):
        """
        Determines the holding period for a ticker

        :param ticker:
        :param holdings_arr:
        :param idx: current month (expressed as an int)
        :return:
        """

        months_held_before = 0

        while True:
            if idx - 1 - months_held_before < 0:
                return months_held_before
            prev_holdings = holdings_arr[idx - 1 - months_held_before]
            if ticker not in prev_holdings:
                break
            else:
                months_held_before += 1

        return months_held_before

if __name__ == '__main__':
    ticker_list = [{'ticker': 'VTI', 'tax_category': 'equities'}]
    tax_config = {'st_gains': 0.35, 'lt_gains': 0.15, 'federal_tax_rate': 0.22,
                   'state_tax_rate': 0.12}
    dmc = DualMomentumComponent(name='equities', ticker_list=ticker_list, lookback_months=12,
                                max_holdings=1, start_date='1980-01-01', use_dual_momentum=True,
                                money_market_holding='VGIT', tax_config=tax_config)
    dmc.run_dual_momentum()
    from IPython import embed
    embed()
