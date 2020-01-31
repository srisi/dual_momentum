from IPython import embed
from dual_momentum.ticker_data import TickerData
from dual_momentum.ticker_config import TICKER_CONFIG
from dual_momentum.dm_config import DATA_PATH
import pandas as pd
from pathlib import Path
import pickle


# def get_tax_rates_by_category(st_gains: float, lt_gains: float, federal_tax_rate: float,
#                   state_tax_rate: float):
def get_tax_rates_by_category(fed_st_gains: float, fed_lt_gains: float, state_st_gains: float,
                              state_lt_gains: float):
    """
    Loads tax rates by investment category

    Income: Dividends and monthly bond payments

    :return: dict
    """


    collectibles_lt = 0.28
    if collectibles_lt > fed_st_gains:
        collectibles_lt = fed_st_gains

    st_gains = state_st_gains + fed_st_gains
    lt_gains = state_lt_gains + fed_lt_gains

    return {
        'equities': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains,   'INCOME': lt_gains},
        'reits': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains,   'INCOME': st_gains},
        'bonds_treasury': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains, 'INCOME': fed_lt_gains},
        'bonds_muni': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains, 'INCOME': state_lt_gains},
        'bonds_other': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains, 'INCOME': st_gains},

        # GLD, SLV etc.
        'collectibles': {'ST_GAINS': st_gains, 'LT_GAINS': collectibles_lt, 'INCOME': st_gains}
    }
    # return {
    #     'equities': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains,   'INCOME': lt_gains},
    #     'reits': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains,   'INCOME': st_gains},
    #     'bonds_treasury': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains, 'INCOME': federal_tax_rate},
    #     'bonds_muni': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains, 'INCOME': state_tax_rate},
    #     'bonds_other': {'ST_GAINS': st_gains,  'LT_GAINS': lt_gains, 'INCOME': st_gains},
    #
    #     # GLD, SLV etc.
    #     'collectibles': {'ST_GAINS': st_gains, 'LT_GAINS': collectibles_lt, 'INCOME': st_gains}
    # }

def get_tax_rates_by_ticker(tax_rates: dict, ticker_list: list):
    """
    returns a dict of tax rates by tickers

    :param tax_rates:
    :param ticker_list:
    :return: dict
    """
    tax_rates_by_ticker = {}

    for t in ticker_list:

        val_error = f'Tax category for {t} available from ticker_config.py. Please pass this ' \
                    f'ticker as a dict with keys ticker and tax_category.'

        # e.g. VTI
        if isinstance(t, str):
            ticker = t
            if ticker in TICKER_CONFIG:
                tax_category = TICKER_CONFIG[ticker]['tax_category']
            else:
                raise ValueError(val_error)
        elif isinstance(t, dict):
            ticker = t['ticker']
            tax_category = t['tax_category']
            if tax_category not in tax_rates:
                raise ValueError(f'Tax category has to be in {tax_rates.keys()}.')
        else:
            raise ValueError(val_error)

        tax_rates_by_ticker[ticker] = tax_rates[tax_category]

    return tax_rates_by_ticker

def load_tbill_rates() -> pd.DataFrame:
    """
    Loads the tbills into a DataFrame
    with columns 'tbil_rate' and 'tbil_performance_1'

    #TODO throw error if data outdated by more than 6 months

    :return: pd.DataFrame
    """
    # delete old (1+ hour) data before trying to load tbil data
    TickerData.delete_old_data()
    pickle_path = Path(DATA_PATH, 'clean_ticker_data', 'TBIL.pickle')

    # try to load data if updated in last hour
    if pickle_path.exists():
        print("load from disk")
        with open(pickle_path, 'rb') as infile:
            return pickle.load(infile)

    # else, generate new data from raw tbil data fram csv
    else:

        rates = pd.read_csv(Path(DATA_PATH, 'index_data', 'tbill_rate.csv'))
        rates['Datetime'] = pd.to_datetime(rates['DATE'])
        rates = rates.set_index('Datetime')
        rates = rates['1980-01-01':]
        rates = rates.groupby(by=[rates.index.year, rates.index.month]).nth(-1)

        rates_df = TickerData('ONES').data_monthly
        rates_df.drop(['Close', 'Adj Close'], inplace=True, axis=1)

        rates_df['tbil_rate'] = rates['TB3MS']

        # figure out where tbil turns into NaN because current data not available
        # and fill up to present
        idx_of_last_data = rates_df['tbil_rate'].last_valid_index()
        rates_df['tbil_rate'].fillna(rates_df['tbil_rate'][idx_of_last_data], inplace=True)

        rates_df['tbil_rate'] += 100
        rates_df['tbil_performance_1'] = (rates_df['tbil_rate'] / 100) ** (1 / 12)

        rates_df.to_pickle(pickle_path)

        return rates_df


if __name__ == '__main__':
    t = load_tbill_rates()
    embed()
