import unittest
from dual_momentum.dm_composite import DualMomentumComposite

import redis
import pandas as pd
from dual_momentum.dm_composite import DualMomentumComponent


class TestBasicDMComponentExample(unittest.TestCase):
    """
    Test that a basic example works
    """

    def setUp(self) -> None:

        self.redis_con = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_con.flushall()

    def tearDown(self):
        self.redis_con.flushall()

    def test_basic_example(self):
        """
        Test that a simple dm_composite example works

        :return:
        """
        ticker_list = ['VNQ', 'VNQI', 'IEF']
        tax_config = {'fed_st_gains': 0.22, 'fed_lt_gains': 0.15, 'state_st_gains': 0.12,
                      'state_lt_gains': 0.051}
        dmc = DualMomentumComponent(name='equities', ticker_list=ticker_list, lookback_months=12,
                                    max_holdings=2, start_date='1980-01-01', use_dual_momentum=True,
                                    money_market_holding='VGIT', tax_config=tax_config)

        dmc.run_dual_momentum()

        self.assertTrue(isinstance(dmc.df, pd.DataFrame))
        self.assertGreater(len(dmc.df), 400)




if __name__ == '__main__':
    # used to test using ipython, which allows using embed in unittests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
