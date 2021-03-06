import unittest
from dual_momentum.rates import get_tax_rates_by_category, get_tax_rates_by_ticker


class TestTaxRatesByTicker(unittest.TestCase):
    """
    Test if passing dict or string with tax config works
    """

    def setUp(self):
        self.tax_config = get_tax_rates_by_category(state_st_gains=0.12, state_lt_gains=0.051,
                                                    fed_st_gains=0.22, fed_lt_gains=0.22)

    def testStr(self):
        """
        Test case where string is passed
        :return:
        """
        ticker_list_in_config = ['VTI', 'VNQ', 'QQQ']
        ticker_list_not_in_config = ['VTI', 'AAPL']

        tax_rates_by_tick = get_tax_rates_by_ticker(self.tax_config, ticker_list_in_config)
        self.assertTrue(isinstance(tax_rates_by_tick, dict))
        self.assertEqual(len(tax_rates_by_tick), 3)
        for ticker in tax_rates_by_tick:
            for rate in ['ST_GAINS', 'LT_GAINS', 'INCOME']:
                self.assertTrue(0 <= tax_rates_by_tick[ticker][rate] <= 1)

        with self.assertRaises(ValueError):
            get_tax_rates_by_ticker(self.tax_config, ticker_list_not_in_config)

    def testDict(self):
        """
        Test case when dict is passed
        :return:
        """

        ticker_list_valid = [{'ticker': 'VTI', 'tax_category': 'equities'},
                             {'ticker': 'QQQ', 'tax_category': 'equities'}]

        tax_rates_by_tick = get_tax_rates_by_ticker(self.tax_config, ticker_list_valid)
        self.assertTrue(isinstance(tax_rates_by_tick, dict))
        self.assertEqual(len(tax_rates_by_tick), 2)
        for ticker in tax_rates_by_tick:
            for rate in ['ST_GAINS', 'LT_GAINS', 'INCOME']:
                self.assertTrue(0 <= tax_rates_by_tick[ticker][rate] <= 1)

        ticker_list_invalid = ticker_list_valid
        ticker_list_invalid[0]['tax_category'] = 'e'
        with self.assertRaises(ValueError):
            get_tax_rates_by_ticker(self.tax_config, ticker_list_invalid)




if __name__ == '__main__':
    unittest.main()




