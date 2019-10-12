import unittest
import time
import numpy as np
from ticker_data import TickerData
from IPython import embed


# class TestTickerData(unittest.TestCase):
#
#
#     def test_force_update(self):
#         """
#         Checks if updating data online actually loads new data
#         :return:
#         """
#
#         data_old = TickerData('SPY', force_new_data=False)
#
#         time.sleep(5)
#         data_disk = TickerData('SPY', force_new_data=False)
#         data_online = TickerData('SPY', force_new_data=True)
#
#         self.assertEqual(data_old, data_disk)
#         self.assertNotEqual(data_old, data_online)

class TestTickerMerge(unittest.TestCase):

    def setUp(self) -> None:

        for ticker, early_replacement in [
            ('SPY', 'VFINX'),
            ('VTI', 'SPY'),
            ('IEFA', 'EFA'),
        ]:
            self.new_merged = TickerData(ticker, use_early_replacements=True).data_daily
            self.old = TickerData(early_replacement, use_early_replacements=True).data_daily
            self.new_no_rep = TickerData(ticker, use_early_replacements=False).data_daily

    def test_merge(self):
        """

        """

        first_index = self.new_no_rep.index[0]
        for c in ['Close', 'Adj Close']:

            # from first shared index on, close and adj close data should be the same
            self.assertTrue(np.allclose(self.new_no_rep[c], self.new_merged[first_index:][c]))

            # check that shift from old to new ticker does not have any unusual returns
            # i.e. when switching from old to new ticker, the return is less than 3%
            ret = (self.new_merged[:first_index][c] / self.new_merged[:first_index][c].shift(
                1)).tail(1)[0]
            self.assertLess(abs(ret - 1), 0.03)

            # check that returns for old and merged ticker are the same at the earliest dates
            # skip first because NaN
            ret_old = (self.old[c] / self.old[c].shift(1)).head()[1:]
            ret_merged = (self.new_merged[c] / self.new_merged[c].shift(1)).head()[1:]
            self.assertTrue(np.allclose(ret_old, ret_merged))


if __name__ == '__main__':
    unittest.main()
