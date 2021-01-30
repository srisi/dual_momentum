import pytest
from dual_momentum.ticker_config import TICKER_CONFIGS

@pytest.mark.parametrize('ticker', TICKER_CONFIGS.keys())
def test_ticker_config(ticker):
    """Test that all ticker configs can be initialized and that early replacement tickers exist."""
    ticker_config = TICKER_CONFIGS[ticker]
    if ticker_config.early_replacement:
        assert ticker_config.early_replacement in TICKER_CONFIGS




