from IPython import embed
from ticker_data import TickerData
from dm_config import DATA_PATH
import pandas as pd
from pathlib import Path
import pickle


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
