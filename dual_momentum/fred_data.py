import csv
from pathlib import Path
from IPython import embed
import datetime
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
from dual_momentum.dm_config import DATA_PATH
from dual_momentum.ticker_data import TickerData


def load_fred_data(name, return_type='dict'):
    """

    :param name:
    :return:
    """

    index_names = {
        'libor_rate':           'USDONTD156N',      # overnight libor
        'tbil_rate':            'TB3MS',            # 3 month t bill rate
        'term_premium_10y':     'ACMTP10',          # 10 year term premium
        'treasuries_10y_yield': 'GS10'              # 10 year constant maturity yield
    }

    if name not in index_names:
        raise ValueError(f'Only {index_names.keys()} can be loaded with load_fred_data, not {name}.')


    index_name = index_names[name]

    file_path = Path(DATA_PATH, 'index_data', f'{index_name}.csv')
    if not file_path.exists():
        if name == 'term_premium_10y':
            download_term_premium_data()
        else:
            download_fred_data(index_name)

    data = {}
    with open(file_path) as csvfile:
        r = csv.reader(csvfile)
        for idx, row in enumerate(r):
            if idx == 0: continue

            year = int(row[0][:4])
            month = int(row[0][5:7])

            # for libor rates, some values are simply periods ('.'). I don't know why
            try:
                val = float(row[1])
            except ValueError:
                continue

            if val == 0:
                continue

            data[(year, month)] = val + 100

    today = datetime.datetime.today()
    last_month_date = today - relativedelta(months=1)

    if not (last_month_date.year, last_month_date.month) in data:

        # data only gets updated after weekend -> wait for 3 days and just duplicate data from
        # previous month.
        if today.day < 5:
            two_months_ago = today - relativedelta(months=2)
            data[(last_month_date.year, last_month_date.month)] = data[(two_months_ago.year,
                                                                        two_months_ago.month)]
        else:
            if name == 'term_premium_10y':
                download_term_premium_data()
            else:
                download_fred_data(index_name)
            return load_fred_data(name)

    # add current month if not in data
    if not (today.year, today.month) in data:
        data[(today.year, today.month)] = data[(last_month_date.year, last_month_date.month)]

    if name == 'libor_rate':
        data = add_libor_rates_before_2001(data)

    if return_type == 'dict':
        return data
    # pandas dataframe
    elif return_type == 'df':
        return parse_data_into_dataframe(file_path, index_name)
    else:
        raise ValueError(f"return_type for load_fred_data has to be 'dict' or 'df' but not "
                         f"{return_type}.")


def parse_data_into_dataframe(file_path, index_name):
    """
    Takes index data and returns it as as a pandas dataframe

    Stores the index in the 'index' column

    :param file_path:
    :return:
    """

    index_df = pd.read_csv(file_path)
    index_df['Datetime'] = pd.to_datetime(index_df['DATE'])
    index_df = index_df.set_index('Datetime')
    index_df = index_df['1980-01-01':]
    index_df = index_df.groupby(by=[index_df.index.year, index_df.index.month]).nth(-1)
    index_df['index'] = index_df[index_name]

    return index_df


def add_libor_rates_before_2001(data):
    """
    Overnight libor rates on FRED only go back to 2001 -> add to 1980 manually

    :param data:
    :return:
    """

    libor_rates = {
        1980: 14.03, 1981: 16.76, 1982: 13.6,
        1983: 9.93, 1984: 11.29, 1985: 8.64, 1986: 6.74, 1987: 7.00, 1988: 7.81,
        1989: 9.28, 1990: 8.25, 1991: 5.92, 1992: 3.74, 1993: 3.20, 1994: 4.47,
        1995: 5.97, 1996: 5.45, 1997: 5.67, 1998: 5.57, 1999: 5.25, 2000: 6.41,
        2001: 3.87, 2002: 1.77, 2003: 1.21, 2004: 1.50, 2005: 3.39, 2006: 5.10,
        2007: 5.25, 2008: 2.68, 2009: 0.33, 2010: 0.27, 2011: 0.23, 2012: 0.24,
        2013: 0.19, 2014: 0.16, 2015: 0.20, 2016: 0.50, 2017: 1.11, 2018: 1.84,
        2019: 2.14, 2020: 2.00
    }

    for year in range(1980, datetime.datetime.today().year + 1):
        for month in range(1, 13):
            if (year, month) not in data:
                data[(year, month)] = libor_rates[year] + 100

    return data

def download_term_premium_data():
    """
    Downloads xls term premium data from https://www.newyorkfed.org/research/data_indicators/term_premia.html

    :return:
    """

    print('Downloading Term Premium Data')
    url = 'https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls'
    df = pd.read_excel(url, sheet_name='ACM Monthly')

    data = []
    for _, row in df.iterrows():
        date = datetime.datetime.strptime(row['DATE'], '%d-%b-%Y').strftime('%Y-%m-%d')
        data.append({
            'DATE': date,   'ACMTP10': row['ACMTP10']
        })

    file_path = Path(DATA_PATH, 'index_data', 'ACMTP10.csv')
    with open(file_path, 'w') as out:
        field_names = ['DATE', 'ACMTP10']
        writer = csv.DictWriter(out, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)


def download_fred_data(index_name):
    """
    Downloads updated FRED data

    :param index_name:
    :return:
    """

    print(f"downloading updated FRED data for {index_name}")
    url = f'http://fred.stlouisfed.org/graph/fredgraph.csv?id={index_name}'

    file_path = Path(DATA_PATH, 'index_data', f'{index_name}.csv')
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    load_fred_data('tbil_rate', return_type='df')
