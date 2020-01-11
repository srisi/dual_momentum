import unittest
import time
import numpy as np
from ticker_data import TickerData
from ticker_config import TICKER_CONFIG
from IPython import embed


class TestTickerMerge(unittest.TestCase):

    def setUp(self) -> None:

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
            self.assertTrue(np.allclose(self.new_no_replacement[c],
                                        self.new_merged[first_index:][c]))

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

    def test_all_keys_available_and_correct(self):
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
                                  ]
            self.assertTrue(ticker_data['early_monthly_index_replacement'] in index_replacements)

            from rates import get_tax_rates_by_category
            tax_categories = get_tax_rates_by_category(0, 0, 0, 0)
            self.assertTrue(ticker_data['tax_category'] in tax_categories)


            #     'name': 'Ones',
            #     'start_year': 1980,
            #     'early_replacement': None,
            #     'early_monthly_index_replacement': None,
            #     'suggest_in_search': False,
            #     'tax_category': 'equities'


if __name__ == '__main__':
    # used to test using ipython, which allows using embed in unittests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
