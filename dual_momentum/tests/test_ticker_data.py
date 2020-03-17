import unittest
import time
import numpy as np
from dual_momentum.ticker_data import TickerData
from dual_momentum.ticker_config import TICKER_CONFIG
from IPython import embed
import pandas as pd

import redis


class TestTickerMerge(unittest.TestCase):

    def setUp(self) -> None:

        self.redis_con = redis.Redis(host='localhost', port=6379, db=1)
        self.redis_con.flushall()

        for ticker, early_replacement in [
            ('SPY', 'VFINX'),
            ('VTI', 'SPY'),
            ('IEFA', 'EFA'),
        ]:
            self.new_no_replacement = TickerData(ticker, use_early_replacements=False).data_daily
            # self.old_no_replacement = TickerData(early_replacement,
            #                                      use_early_replacements=False).data_daily
            self.new_merged = TickerData(ticker, use_early_replacements=True).data_daily
            self.old = TickerData(early_replacement, use_early_replacements=True).data_daily

            self.test_using_replacements_works()
            self.test_merge()

    def tearDown(self):
        self.redis_con.flushall()

    def test_using_replacements_works(self):
        """
        Check if using and not using replacements produces different dataframes

        :return:
        """
        self.assertNotEqual(len(self.new_no_replacement), len(self.new_merged))


    def test_merge(self):
        """
        Test if ticker merging works
        """

        first_index = self.new_no_replacement.index[0]

        print(first_index)
        for c in ['Close', 'Adj Close']:

            # from first shared index on, close and adj close data should be the same
            self.assertTrue(np.allclose(self.new_no_replacement[c][:-1],
                                        self.new_merged[first_index:][c][:-1]))

            # last number should be within 0.1% of each other but not exactly equal as data might
            # have been updated in the meantime
            self.assertTrue(abs((self.new_no_replacement[c][-1] / self.new_merged[c][-1]) -1) <
                            0.001)

            # check that shift from old to new ticker does not have any unusual returns
            # i.e. when switching from old to new ticker, the return is less than 3%
            ret = (
                self.new_merged[:first_index][c] / self.new_merged[:first_index][c].shift(1)
                ).tail(1)[0]

            self.assertLess(abs(ret - 1), 0.03)

            # check that returns for old and merged ticker are the same at the earliest dates
            # skip first because NaN
            ret_old = (self.old[c] / self.old[c].shift(1)).head()[1:]
            ret_merged = (self.new_merged[c] / self.new_merged[c].shift(1)).head()[1:]
            self.assertTrue(np.allclose(ret_old, ret_merged))

class TestTickerConfig(unittest.TestCase):
    """
    Test if the configuration for each ticker in ticker_config is complete
    test if all tickers can be loaded

    """
    def setUp(self):
        self.redis_con = redis.Redis(host='localhost', port=6379, db=1)
        self.redis_con.flushall()

    def tearDown(self):
        self.redis_con.flushall()

    def test_all_keys_available_and_correct(self):
        """
        Test if the config for all tickers is complete
        """
        for ticker in TICKER_CONFIG:

            ticker_data = TICKER_CONFIG[ticker]
            for key in ['name', 'start_year', 'early_replacement',
                        'early_monthly_index_replacement', 'suggest_in_search',
                        'tax_category']:
                try:
                    self.assertTrue(key in ticker_data)
                except AssertionError:
                    print(key, ticker, ticker_data)
                    raise(AssertionError)

            self.assertTrue(isinstance(ticker_data['name'], str))
            self.assertTrue(isinstance(ticker_data['start_year'], int))
            self.assertTrue(ticker_data['early_replacement'] in list(TICKER_CONFIG.keys()) + [None])
            self.assertTrue(ticker_data['suggest_in_search'] in {True, False})

            index_replacements = [None, 'alpha_architect.csv', 'eq_reit.csv', 'eq_vmot.csv',
                                  'mortgage_reit.csv', 'gold_bullion.csv']
            self.assertTrue(ticker_data['early_monthly_index_replacement'] in index_replacements)

            from dual_momentum.rates import get_tax_rates_by_category
            tax_categories = get_tax_rates_by_category(0, 0, 0, 0)
            self.assertTrue(ticker_data['tax_category'] in tax_categories)

    def test_load_all_tickers(self):
        """
        Test if all tickers can be loaded from yahoo
        """
        for ticker in TICKER_CONFIG:
            if ticker == 'TBIL':
                continue
            loaded_ticker_data = TickerData(ticker)
            self.assertTrue(isinstance(loaded_ticker_data.data_daily, pd.DataFrame))
            self.assertGreater(len(loaded_ticker_data.data_daily), 4)

            self.assertTrue(isinstance(loaded_ticker_data.data_monthly, pd.DataFrame))
            self.assertGreater(len(loaded_ticker_data.data_monthly), 4)


if __name__ == '__main__':
    # used to test using ipython, which allows using embed in unittests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
