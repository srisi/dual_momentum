from datetime import date
from pathlib import Path
import os
import time
import pickle

import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
from IPython import embed
from dual_momentum.ticker_config import TICKER_CONFIG


class TickerData:


    def __init__(self, ticker, use_early_replacements=True, force_new_data=False,
                 day_of_month_for_monthly_data=-1,
                 is_replacement_ticker=False
                 ):
        """
        TickerData class holds daily and monthly information for one ticker


        :param ticker: str
        :param use_early_replacements: bool. Whether or not to use early replacements to generate
                                             longer historical series going back to 1980
        :param force_new_data: bool. Force download of new data
        :param day_of_month_for_monthly_data: When turning daily into monthly data, what day should
                                              be used? Default: -1, last trading day of the month
        :param is_replacement_ticker: Is this an early replacement ticker? If so, data needs to be
                                      from today but not from the last hour.
        """

        self.ticker = ticker
        self.name = TICKER_CONFIG[ticker]['name']
        self.start_year = TICKER_CONFIG[ticker]['start_year']
        self.early_replacement = TICKER_CONFIG[ticker]['early_replacement']
        self.monthly_index_replacement = TICKER_CONFIG[ticker][
            'early_monthly_index_replacement']
        self.tax_category = TICKER_CONFIG[ticker]['tax_category']
        self.use_early_replacements = use_early_replacements
        self.force_new_data = force_new_data
        self.is_replacement_ticker = is_replacement_ticker
        self.day_of_the_month_for_monthly_data = day_of_month_for_monthly_data

        self._data_daily = None
        self._data_monthly = None


    @property
    def data_daily(self) -> pd.DataFrame:
        """
        Returns a datafram with daily ticker data

        :return:
        """

        if self._data_daily is not None:
            return self._data_daily

        # if pickle data stored in the last hour, or last day for replacement ticker, load it
        if not self.force_new_data and (
            file_exists_and_less_than_1hr_old(self.file_path_daily) or
            (self.is_replacement_ticker and file_exists_and_is_from_today(self.file_path_daily))
        ):
            self._data_daily = pd.read_pickle(self.file_path_daily)

        else:
            self.load_ticker_data() # loads data and updates self._data_daily
            self._data_daily.to_pickle(self.file_path_daily)

        return self._data_daily

    @property
    def data_monthly(self) -> pd.DataFrame:
        """
        Returns a dataframe with monthly ticker data (based on selected day_of_the_month).

        :return:
        """

        if self._data_monthly is not None:
            return self._data_monthly

        # if pickle data stored in the last hour, or last day for replacement ticker, load it
        if not self.force_new_data and (
            file_exists_and_less_than_1hr_old(self.file_path_monthly) or
            (self.is_replacement_ticker and file_exists_and_is_from_today(self.file_path_monthly))
        ):
            self._data_monthly = pd.read_pickle(self.file_path_monthly)

        else:
            # update data_monthly in case the stored version had a different day_of_month...
            self._data_monthly = self.data_daily.groupby(
                by=[self.data_daily.index.year,self.data_daily.index.month]).nth(
                self.day_of_the_month_for_monthly_data)
            if self.monthly_index_replacement:
                self.merge_monthly_data_with_index(self.monthly_index_replacement)

            self._data_monthly.to_pickle(self.file_path_monthly)

        return self._data_monthly

    def __eq__(self, other):
        return (
            self.ticker == other.ticker and
            self.use_early_replacements == other.use_early_replacements and
            np.all(self.data_daily == other.data_daily) and
            np.all(self.data_monthly == other.data_monthly)
        )

    def __repr__(self):
        return str(self.data_daily)

    @property
    def file_path_daily(self):
        """
        Path to the daily data (stored as pd Dataframe)
        :return:
        """
        return Path(DATA_PATH, 'ticker_data_daily',
             f'{self.ticker}_replacement_{self.use_early_replacements}.pickle')

    @property
    def file_path_monthly(self):
        """
        Path to the monthly data (stored as pd Dataframe)
        :return:
        """
        return Path(DATA_PATH, 'ticker_data_monthly',
             f'{self.ticker}_replacement_{self.use_early_replacements}'
             f'_last_{self.day_of_the_month_for_monthly_data}.pickle')

    @property
    def file_path_raw_yahoo_data(self):
        """
        Path to the raw, unprocessed yahoo data (stored as pd Dataframe)
        :return:
        """
        return Path(DATA_PATH, 'ticker_data_raw_yahoo', f'{self.ticker}.pickle')

    def load_ticker_data(self):
        """
        Load the daily data for one ticker including early replacements where necessary.

        :return:
        """

        # if just all ones -> load ticker going to 1980 and set it to all ones.
        if self.ticker == 'ONES':
            self._data_daily = TickerData(ticker='SPY',
                                    force_new_data=self.force_new_data,
                                    is_replacement_ticker=True).data_daily
            self._data_daily['Adj Close'] = 1.00
            self._data_daily['Close'] = 1.00

        else:
            self._data_daily = self.load_raw_data_or_get_from_yahoo()

            # if we use early replacements, merge daily data with the replacements.
            if self.use_early_replacements and self.early_replacement:
                self.merge_daily_data_with_early_replacements()

    def merge_daily_data_with_early_replacements(self):
        """
        Merges a ticker with its earlier replacements going back to 1980 where possible
        If no early replacement, does nothing

        """
        # load the data for the early replacement
        early_stock_data = TickerData(self.early_replacement,
                                      force_new_data=self.force_new_data,
                                      use_early_replacements=True).data_daily

        # adjust stock closing price of replacement for a seamless transition to the new ticker.
        first_date = self._data_daily.index[0]
        for c in ['Close', 'Adj Close']:
            early_stock_data[c] *= (self._data_daily[c][first_date] / early_stock_data[c][
                first_date])

        # [:-1] to avoid duplicating the first date
        early_stock_data = early_stock_data[:first_date][:-1]
        self._data_daily = early_stock_data.append(self._data_daily[first_date:], sort=True)
        self._data_daily = self._data_daily['1980-01-01':]

    def merge_monthly_data_with_index(self, index_csv_name: str):
        """

        :param index_csv_name:
        :return:
        """

        # load index and convert to monthly data
        index_data = pd.read_csv(Path(DATA_PATH, 'index_data', index_csv_name))
        index_data['Datetime'] = pd.to_datetime(index_data['Date'])
        index_data = index_data.set_index('Datetime')
        index_data = index_data['1980-01-01':]
        index_data = index_data.groupby(by=[index_data.index.year,
                                            index_data.index.month]).nth(-1)

        first_date = self._data_monthly.index[0]
        merged_monthly_data = TickerData('ONES').data_monthly

        for c in ['Close', 'Adj Close']:
            if self.ticker in ['QVAL', 'IVAL', 'QMOM', 'IMOM']:
                index_data[c] = index_data[f'{self.ticker}_index']

            # adjust index data to fit with ticker monthly data
            index_data[c] *= (self._data_monthly[c][first_date] / index_data[c][first_date])

            # set merged data until first date to index data
            merged_monthly_data[c][:first_date] = index_data[c][:first_date]
            # for the rest, use ticker data
            merged_monthly_data[c][first_date:] = self._data_monthly[c][first_date:]

        self._data_monthly = merged_monthly_data

    def load_raw_data_or_get_from_yahoo(self):
        """
        Loads raw yahoo ticker data either from disk or from yahoo

        :param ticker:
        :param force_new_data: bool
        :param multiprocessing.Queue
        :return:
        """

        if not self.force_new_data and (
            file_exists_and_less_than_1hr_old(self.file_path_raw_yahoo_data) or
            (self.is_replacement_ticker and
             file_exists_and_is_from_today(self.file_path_raw_yahoo_data))
        ):
            print(self.ticker, "disk")
            stock_data = pd.read_pickle(self.file_path_raw_yahoo_data)

        else:
            print(self.ticker, "yahoo")
            while True:
                try:
                    start_date = '1/1/1980'
                    stock_data = web.DataReader(self.ticker, data_source='yahoo', start=start_date,
                                                end=date.today())
                    stock_data.drop(['Open', 'High', 'Low', 'Volume'], inplace=True, axis=1)
                    stock_data.to_pickle(self.file_path_raw_yahoo_data)
                    break

                except pdr._utils.RemoteDataError as e:
                    print(self.ticker, date)
                    print(e)

        return stock_data


if __name__ == "__main__":
    t = TickerData('GLD', force_new_data=False, use_early_replacements=True).data_monthly
    print(t)
