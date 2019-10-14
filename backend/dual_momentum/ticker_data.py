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
from dm_config import DATA_PATH
from ticker_config import TICKER_CONFIG


class TickerData:

    def __init__(self, ticker, use_early_replacements=True, force_new_data=False,
                 day_of_month_for_monthly_data=-1):

        # delete all ticker data older than 1 hour
        self.delete_old_data()

        pickle_path = Path(DATA_PATH, 'clean_ticker_data', f'{ticker}.pickle')

        # if pickle data stored in the last hour, load it.
        if not force_new_data and pickle_path.exists():
            with open(pickle_path, 'rb') as infile:
                loaded_ticker_data = pickle.load(infile)
            self.__dict__.update(loaded_ticker_data.__dict__)
            print("loaded from disk")

        # otherwise, create it anew.
        else:
            self.ticker = ticker
            self.name = TICKER_CONFIG[ticker]['name']
            self.start_year = TICKER_CONFIG[ticker]['start_year']
            self.early_replacement = TICKER_CONFIG[ticker]['early_replacement']
            self.monthly_index_replacement = TICKER_CONFIG[ticker][
                'early_monthly_index_replacement']
            self.tax_category = TICKER_CONFIG[ticker]['tax_category']

            self.use_early_replacements = use_early_replacements
            self.force_new_data = force_new_data

            self.data_daily = self.load_ticker_data()
            self.data_monthly = self.data_daily.groupby(by=[self.data_daily.index.year,
                                                            self.data_daily.index.month]).nth(
                day_of_month_for_monthly_data)
            if self.monthly_index_replacement:
                self.data_monthly = self.merge_monthly_data_with_index(
                    self.monthly_index_replacement)

            with open(pickle_path, 'wb') as outfile:
                pickle.dump(self, outfile, protocol=pickle.HIGHEST_PROTOCOL)

    def __eq__(self, other):
        return (
            self.ticker == other.ticker and
            self.use_early_replacements == other.use_early_replacements and
            np.all(self.data_daily == other.data_daily) and
            np.all(self.data_monthly == other.data_monthly)
        )

    def __repr__(self):
        return str(self.data_daily)

    @staticmethod
    def delete_old_data():
        """
        Deletes all ticker data older than 1 hour

        :return:
        """
        for p in ['clean_ticker_data', 'stock_data']:
            directory = Path(DATA_PATH, p)
            for file in os.listdir(directory):
                file_path = Path(directory, file)
                if time.time() - os.path.getmtime(file_path) > 3600:
                    print(file_path)
                    os.remove(file_path)

    def load_ticker_data(self):
        """
        Load the daily data for one ticker including early replacements where necessary.

        :return:
        """

        # if just all ones -> load ticker going to 1980 and set it to all ones.
        if self.ticker == 'ONES':
            data_daily = TickerData('SPY', force_new_data=self.force_new_data).data_daily
            data_daily['Adj Close'] = 1.00
            data_daily['Close'] = 1.00
            return data_daily

        else:
            data_daily = self.load_data_from_disk(self.ticker, self.force_new_data)
            print("disk", self.ticker, len(data_daily))

            # if we use early replacements, merge daily data with the replacements.
            if self.use_early_replacements and self.early_replacement:
                data_daily = self.merge_daily_data_with_early_replacements(data_daily)

        print(self.ticker, len(data_daily))
        return data_daily

    def merge_daily_data_with_early_replacements(self, data_daily: pd.DataFrame) -> pd.DataFrame:
        """
        Merges a ticker with its earlier replacements going back to 1980 where possible
        If no early replacement, does nothing

        """
        # load the data for the early replacement
        early_stock_data = TickerData(self.early_replacement,
                                      force_new_data=self.force_new_data,
                                      use_early_replacements=True).data_daily

        # adjust stock closing price of replacement for a seamless transition to the new ticker.
        first_date = data_daily.index[0]
        for c in ['Close', 'Adj Close']:
            early_stock_data[c] *= (data_daily[c][first_date] / early_stock_data[c][first_date])

        # [:-1] to avoid duplicating the first date
        early_stock_data = early_stock_data[:first_date][:-1]
        data_daily = early_stock_data.append(data_daily[first_date:], sort=True)
        data_daily = data_daily['1980-01-01':]
        return data_daily

    def merge_monthly_data_with_index(self, index_csv_name: str) -> pd.DataFrame:
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

        first_date = self.data_monthly.index[0]
        merged_monthly_data = TickerData('ONES').data_monthly

        for c in ['Close', 'Adj Close']:
            if self.ticker in ['QVAL', 'IVAL', 'QMOM', 'IMOM']:
                index_data[c] = index_data[f'{self.ticker}_index']

            # adjust index data to fit with ticker monthly data
            index_data[c] *= (self.data_monthly[c][first_date] / index_data[c][first_date])

            # set merged data until first date to index data
            merged_monthly_data[c][:first_date] = index_data[c][:first_date]
            # for the rest, use ticker data
            merged_monthly_data[c][first_date:] = self.data_monthly[c][first_date:]

        return merged_monthly_data

    @staticmethod
    def load_data_from_disk(ticker, force_new_data):
        """
        Loads data for a ticker from disk. If not available, loads from yahoo and stores locally
        Use force_new_data to force downloading new data

        :param ticker:
        :param force_new_data: bool
        :return:
        """
        pickle_name = '{}_{}.pickle'.format(ticker, date.today().strftime('%Y-%m-%d'))
        pickle_path = Path(DATA_PATH, 'stock_data', pickle_name)

        if pickle_path.exists() and not force_new_data:
            stock_data = pd.read_pickle(pickle_path)

        else:
            while True:
                try:
                    start_date = '1/1/1980'
                    stock_data = web.DataReader(ticker, data_source='yahoo', start=start_date,
                                                end=date.today())
                    stock_data.drop(['Open', 'High', 'Low', 'Volume'], inplace=True, axis=1)
                    stock_data.to_pickle(pickle_path)
                    break
                except pdr._utils.RemoteDataError as e:
                    print(ticker, date)
                    print(e)

        return stock_data


if __name__ == "__main__":
    t = TickerData('VMOT', force_new_data=False, use_early_replacements=True)
