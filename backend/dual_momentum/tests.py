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




if __name__ == '__main__':
    unittest.main()
