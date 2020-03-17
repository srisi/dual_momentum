import unittest
from dual_momentum.dm_composite import DualMomentumComposite

import redis
import pandas as pd


class TestBasicDMCompositeExample(unittest.TestCase):
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
        tax_config = {'fed_st_gains': 0.22, 'fed_lt_gains': 0.15, 'state_st_gains': 0.12,
                      'state_lt_gains': 0.051}
        money_market_holding = 'VGIT'
        start_date = '1980-01-01'
        leverage = 1
        borrowing_cost_above_libor = 1.5
        parts = [
            {
                'name': 'equities',
                'ticker_list': ['VTI', 'QQQ', 'IEMG', 'IEFA'],
                'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 2, 'weight': 0.5
            },
            {
                'name': 'reits',
                'ticker_list': ['VNQ', 'VNQI', 'REM'],
                'lookback_months': 12, 'use_dual_momentum': True, 'max_holdings': 1, 'weight': 0.5
            }
        ]

        momentum_leverages = {
            'months_for_lev': 3,
            0.80: -0.3, 0.85: -0.3, 0.90: -0.2, 0.95: -0.2,
            1.30: 0.2, 1.20: 0.1, 1.15: 0.1, 1.10: 0.0, 1.05: 0.0
        }

        dm = DualMomentumComposite(parts=parts, money_market_holding=money_market_holding,
                                   momentum_leverages=momentum_leverages, tax_config=tax_config,
                                   start_date=start_date,
                                   leverage=leverage,
                                   borrowing_cost_above_libor=borrowing_cost_above_libor,
                                   force_new_data=False)

        dm.run_multi_component_dual_momentum()
        dm.generate_results_summary()

        self.assertTrue(isinstance(dm.df, pd.DataFrame))
        self.assertGreater(len(dm.df), 400)

        # random example to see if summary was generated properly
        self.assertTrue(0 < dm.summary['max_dd_strategy_pretax'] < 1 )




if __name__ == '__main__':
    # used to test using ipython, which allows using embed in unittests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
