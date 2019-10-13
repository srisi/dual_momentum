from rates import load_tbill_rates
from ticker_data import TickerData
import re
import numpy as np


class DualMomentumComponent:
    """
    DualMomentumComponent simulates one DM component, e.g. equities or REITs
    """

    def __init(self, name: str, ticker_list: list, lookback_months: int, max_holdings: int,
               start_date: str, use_dual_momentum: bool, money_market_holding: str,
               force_new_data: bool = False, use_early_replacements: bool = True,
               day_of_month_for_monthly_data: int = -1):


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

        if self.money_market_holding != 'TBIL':
            self.add_ticker_to_df(self.money_market_holding)

        for ticker in self.ticker_list:
            self.add_ticker_to_df(ticker)

        # Find stock with highest momentum during the lookback period and 
        self.df['max_mom'] = self.df['tbil_rate']
        for ticker in self.ticker_list:
            self.df['max_mom'] = np.where(
                (self.df['{}_mom'.format(ticker)] > self.df['max_mom']),
                 self.df['{}_mom'.format(ticker)], self.df['max_mom'])

        # Find the stock held (i.e. the one, matching the momentum of max_mom_12
        all_stocks['holding'] = 'tbil'
        for ticker in ticker_list:
            all_stocks['holding'] = np.where(
                all_stocks['max_mom'] == all_stocks['{}_mom'.format(ticker)],
                ticker,
                all_stocks['holding'])

    def add_ticker_to_df(self, ticker):
        """
        Adds a ticker to the dataframe
        :param ticker: str
        :return:
        """

        new_stock = TickerData(ticker=ticker, use_early_replacements=self.use_early_replacements,
                               force_new_data=self.force_new_data,
                               day_of_month_for_monthly_data=self.day_of_month_for_monthly_data)

        # calculate and store momentum of ticker
        self.df['{}_mom'.format(ticker)] = 0



        for month in duration:

            try:
                df['{}_mom'.format(ticker)] += new_stock['Adj Close'] / new_stock[
                    'Adj Close'].shift(month) * 100
                df['{}_ma'.format(ticker)] += new_stock['Adj Close'] / new_stock[
                    'Adj Close'].rolling(12).mean() * 100
            except (ValueError, KeyError):
                df['{}_mom'.format(ticker)] = new_stock['Adj Close'] / new_stock['Adj Close'].shift(
                    month) * 100
                df['{}_ma'.format(ticker)] = new_stock['Adj Close'] / new_stock[
                    'Adj Close'].rolling(12).mean() * 100

            except:
                print("in add_ticker_to_df")

        df['{}_mom'.format(ticker)] /= len(duration)
        df['{}_close'.format(ticker)] = new_stock['Adj Close']
        df['{}_performance_1'.format(ticker)] = df['{}_close'.format(ticker)].shift(-1) / df[
            '{}_close'.format(ticker)]


