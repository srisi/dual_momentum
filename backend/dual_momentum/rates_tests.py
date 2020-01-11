import unittest
from rates import get_tax_rates_by_category, get_tax_rates_by_ticker


class TestTaxRatesByTicker(unittest.TestCase):

    def setUp(self):
        self.tax_config = get_tax_rates_by_category(st_gains=0.35, lt_gains=0.15,
                                                    federal_tax_rate=0.22, state_tax_rate=0.12)

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




