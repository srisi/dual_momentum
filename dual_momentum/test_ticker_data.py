import pytest
from dual_momentum.ticker_data import TickerData
from pandas.core.frame import DataFrame
import pandas_datareader.data as datareader_web
import pandas_datareader as pdr
import time
import numpy as np
import pandas as pd
from datetime import date, timedelta

from dual_momentum.ticker_config import TICKER_CONFIGS


@pytest.fixture()
def test_ticker():
    t = TickerData(ticker='SPY', force_new_data=True, use_early_replacements=False)
    yield t
    t.file_path_raw_yahoo_data.unlink(missing_ok=True)


class TestTickerMerge:

    @pytest.mark.parametrize(
        'ticker', [t for t in TICKER_CONFIGS if TICKER_CONFIGS[t].early_replacement]
    )
    def test_merge_daily(self, ticker):
        """Test that merging daily data works.

        Tests:
        a) less than 4 days between date before and after merge
        b) data equal after merge for ticker with or without replacement
        c) returns equal for early replacement and ticker with replacement until replacement date
        d) returns on merge day less than 3.5% (VEA is about 3.5% on merge day)."""

        ticker_no_replacement = TickerData(ticker, use_early_replacements=False)
        ticker_with_replacement = TickerData(ticker, use_early_replacements=True)
        early_replacement = TickerData(
            ticker_with_replacement.early_replacement, use_early_replacements=True
        )

        # remove existing daily data
        ticker_no_replacement.file_path_daily.unlink(missing_ok=True)
        ticker_with_replacement.file_path_daily.unlink(missing_ok=True)
        early_replacement.file_path_daily.unlink(missing_ok=True)

        data_no_replacement = ticker_no_replacement.data_daily
        data_with_replacement = ticker_with_replacement.data_daily
        data_early_replacement = early_replacement.data_daily

        assert len(data_with_replacement) > len(data_no_replacement)

        # find date of first close of ticker as well as day before
        first_date_of_ticker = data_no_replacement.index[0]
        idx_first_date = data_with_replacement.index.tolist().index(first_date_of_ticker)
        last_date_before_ticker = data_with_replacement.index.tolist()[idx_first_date - 1]

        # first date of ticker and last day before should not be more than 1 long weekend apart.
        assert first_date_of_ticker - last_date_before_ticker < pd.Timedelta(days=4)

        for c in ['Close', 'Adj Close']:

            # from first shared index on, close and adj close data should be the same
            assert np.allclose(
                data_no_replacement[c],
                data_with_replacement[first_date_of_ticker:][c]
            )

            # check that shift from old to new ticker does not have any unusual returns
            # i.e. when switching from old to new ticker, the return is less than 3.5%
            value_before_shift = data_with_replacement[c].at[last_date_before_ticker]
            value_after_shift = data_with_replacement[c].at[first_date_of_ticker]
            return_during_shift = value_after_shift / value_before_shift
            assert abs(return_during_shift - 1) < 0.035

            # check that returns for old and merged ticker are the same until merge date
            values_early_replacement = data_early_replacement[c][:last_date_before_ticker]
            returns_early_replacement = values_early_replacement / values_early_replacement.shift(1)
            values_merged_ticker = data_with_replacement[c][:last_date_before_ticker]
            returns_merged_ticker = values_merged_ticker / values_merged_ticker.shift(1)
            # skip first because NaN
            assert np.allclose(returns_early_replacement[1:], returns_merged_ticker[1:])

    @pytest.mark.parametrize(
        'ticker', [t for t in TICKER_CONFIGS if TICKER_CONFIGS[t].early_monthly_index_replacement]
    )
    def test_merge_monthly(self, ticker):
        """Test that merge monthly runs correctly for all tickers that use it.

        Checks:
        a) there are no gaps between the month before ticker went live and start of ticker
        b) abs(return) during merge < 7%
        c) all months represented in monthly data
        """

        ticker_data = TickerData(ticker, use_early_replacements=False)

        # remove any existing monthly data so that it has to be regenerated.
        ticker_data.file_path_monthly.unlink(missing_ok=True)
        ticker_data.data_daily  # load daily data
        monthly_data_without_index = ticker_data.data_daily.groupby(
            by=[ticker_data.data_daily.index.year, ticker_data.data_daily.index.month]).nth(
                ticker_data.day_of_the_month_for_monthly_data).copy()
        # accessing monthly data automatically merges ticker with index data
        monthly_data_with_index = ticker_data.data_monthly

        first_month_of_ticker = monthly_data_without_index.index[0]
        idx_first_date = monthly_data_with_index.index.tolist().index(first_month_of_ticker)
        last_month_before_ticker = monthly_data_with_index.index.tolist()[idx_first_date - 1]

        # first_month_of_ticker should be one month after last_month_before_ticker
        after = date(year=first_month_of_ticker[0], month=first_month_of_ticker[1], day=1)
        before = date(year=last_month_before_ticker[0], month=last_month_before_ticker[1], day=1)
        assert timedelta(days=1) <= after - before <= timedelta(days=31)


        for c in ['Close', 'Adj Close']:
            # no monthly index moved more than 7% during the shift
            value_before_shift = monthly_data_with_index[c].at[first_month_of_ticker]
            value_after_shift = monthly_data_with_index[c].at[last_month_before_ticker]
            return_during_shift = value_after_shift / value_before_shift
            assert abs(return_during_shift - 1) < 0.07

            # after shift, no difference between with or without index
            with_index_after_shift = monthly_data_with_index[c][first_month_of_ticker:]
            without_index_after_shift = monthly_data_with_index[c][first_month_of_ticker:]
            assert np.allclose(with_index_after_shift, without_index_after_shift)

        # Monthly data with index should be as long as monthly data generated from a mutual fund
        # going back to 1980.
        vfinx = TickerData('VFINX', use_early_replacements=True)
        assert len(vfinx.data_monthly) == len(monthly_data_with_index)



class TestFetchAndStoreDataFromYahoo:

    def test_fetching_from_yahoo_works(self, test_ticker):

        fetched_data = test_ticker.fetch_and_store_data_from_yahoo()
        assert isinstance(fetched_data, DataFrame)
        assert str(fetched_data.index[0]) == '1993-01-29 00:00:00'
        assert len(fetched_data) > 7000

    @pytest.mark.parametrize('exception', [pdr._utils.RemoteDataError, ValueError])
    def test_fetching_from_yahoo_has_not_infinite_attempts(
        self, monkeypatch, test_ticker, exception
    ):
        """Previously, fetching a ticker could get stuck in an infinite loop and the IP get
        banned by yahoo for too many requests."""

        def DataReader(*args, **kwargs):
            raise exception
        monkeypatch.setattr(datareader_web, 'DataReader', DataReader)

        start_time = time.time()

        with pytest.raises(exception):
            test_ticker.fetch_and_store_data_from_yahoo(
                max_attempts=10, timeout_between_attempts=0
            )

        # 10 attempts with 0 sleep should take less than 1 second.
        assert time.time() - start_time < 1
