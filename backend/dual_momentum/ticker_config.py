


TICKER_CONFIG = {

    'ONES': {
        'name': 'Ones',
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },

    # U.S. Stock Market
    'VTI':  {
        'name': 'U.S. Stock Market',
        'name_full': 'Vanguard Total Stock Market Index Fund ETF',
        'start_year': 2001,
        'early_replacement': 'SPY',     # less broad market but good replacement
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'SPY': {
        'name': 'S&P 500',
        'name_full': 'SPDR S&P 500 ETF ',
        'start_year': 1993,
        'early_replacement': 'VFINX',   # the same, just mutual fund
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'VFINX': {
        'name': 'S&P 500 Mutual Fund',
        'name_full': 'Vanguard 500 Index Fund',
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'QQQ': {
        'name': 'Nasdaq 100',
        'name_full': 'Invesco QQQ Trust',
        'start_year': 1999,
        'early_replacement': 'RYOCX',   # the same, just mutual fund
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'RYOCX': {
        'name': 'Nasdaq 100 Mutual Fund',
        'name_full': 'Rydex NASDAQ-100 Fund',
        'start_year': 1994,
        'early_replacement': 'ONES',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },

    # U.S. ESG
    'ESGV': {
        'name': 'U.S. ESG Stocks',
        'name_full': 'Vanguard Environmental, Social and Governance U.S. Stock ETF',
        'start_year': 2018,
        'early_replacement': 'VFTSX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'VFTSX': {
        'name': 'Vanguard FTSE Social Index Fund',
        'start_year': 2000,
        'early_replacement': 'VTI',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },



    # Developed Markets
    'IEFA': {
        'name': 'Developed Stock Markets (EAFE)',
        'start_year': 2012,
        'early_replacement': 'EFA',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'EFA': {
        'name': 'Developed Stock Markets (EAFE)',
        'start_year': 2001,
        'early_replacement': 'AAIEX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'AAIEX': {
        'name': 'American Beacon International Equity',
        'start_year': 1996,
        'early_replacement': 'OPPAX',   # pretty similar but not exact
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'OPPAX': {
        'name': 'Oppenheimer Global Fund', # caught up in dot com bubble
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'VEA': {
        'name': 'Developed Stock Markets',
        'name_full': 'Vanguard FTSE Developed Markets Index Fund ETF',
        'start_year': 2007,
        'early_replacement': 'EFA',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },

    # Developing Markets

    'IEMG': {
        'name': 'Emerging Stock Markets',
        'name_full': 'iShares Core MSCI Emerging Markets ETF',
        'start_year': 2012,
        'early_replacement': 'EEM',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'EEM': {
        'name': 'iShares MSCI Emerging Markets ETF',
        'start_year': 2003,
        'early_replacement': 'TWMIX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'TWMIX': {
        'name': 'American Century Emerging Markets Fund',
        'start_year': 1997,
        'early_replacement': 'MADCX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'MADCX': {
        'name': 'BlackRock Emerging Markets Fund, Inc.',
        'start_year': 1989,
        'early_replacement': 'ONES',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'VWO': {
        'name': 'Vanguard FTSE Emerging Markets Index Fund',
        'start_year': 2005,
        'early_replacement': 'EEM',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },

    # Low Volatility

    'USMV': {
        'name': 'U.S. Low Volatility Stocks',
        'name_full': 'iShares Edge MSCI Min Vol USA ETF',
        'start_year': 2011,
        'early_replacement': 'SPLV',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'SPLV': {
        'name': 'iShares Edge MSCI Min Vol USA',
        'start_year': 2011,
        'early_replacement': 'VTI',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'EFAV': {
        'name': 'Developed Markets Low Volatility Stocks',
        'name_full': 'iShares Edge MSCI Min Vol EAFE ETF',
        'start_year': 2011,
        'early_replacement': 'EFA',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'EEMV': {
        'name': 'Developing Markets Low Volatility Stocks',
        'start_year': 2011,
        'early_replacement': 'EEM',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },

    # Small Caps
    'VB': {
        'name': 'U.S. Small Caps Stocks',
        'name_full': 'Vanguard Small-Cap Index Fund ETF',
        'start_year': 2004,
        'early_replacement': 'NAESX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'NAESX': {
        'name': 'Vanguard Small Capitalization Index Fund',
        'start_year': 1980,
        'early_replacement': 'ONES',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },

    'VSS': {
        'name': 'All World ex-U.S. Small Caps Stocks',
        'name_full': 'Vanguard Small Capitalization Index Fund',
        'start_year': 2009,
        'early_replacement': 'VINEX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'VINEX': {
        'name': 'Vanguard International Explorer Fund',
        'start_year': 1996,
        'early_replacement': 'ONES',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },


    # REITs
    'VNQ': {
        'name': 'U.S. Equities REITs',
        'start_year': 2004,
        'early_replacement': 'RWR',
        'early_monthly_index_replacement': 'eq_reit.csv',
        'suggest_in_search': True,
        'tax_category': 'reits'
    },
    'RWR': {
        'name': 'U.S. Equities REITs',
        'start_year': 2001,
        'early_replacement': 'DFREX',
        'early_monthly_index_replacement': 'eq_reit.csv',
        'suggest_in_search': False,
        'tax_category': 'reits'
    },
    'DFREX': {
        'name': 'DFA Real Estate Securities',
        'start_year': 1993,
        'early_replacement': None,
        'early_monthly_index_replacement': 'eq_reit.csv',
        'suggest_in_search': False,
        'tax_category': 'reits'
    },


    'VNQI': {
        'name': 'International Equities REITs',
        'start_year': 0000,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'reits'
    },

    # Alpha Architect
    'VMOT': {
        'name': 'Alpha Architect Value Momentum Trend',
        'start_year': 2017,
        'early_replacement': None,
        'early_monthly_index_replacement': 'eq_vmot.csv',
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'QVAL': {
        'name': 'U.S. Quantitative Value',
        'start_year': 2014,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'IVAL': {
        'name': 'International Quantitative Value',
        'start_year': 2014,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'QMOM': {
        'name': 'U.S. Quantitative Momentum',
        'start_year': 2015,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'IMOM': {
        'name': 'International Quantitative Momentum',
        'start_year': 2015,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True,
        'tax_category': 'equities'
    },

    # Treasuries
    'VGIT': {                                                   # duration: 5.14 years
        'name': 'Intermediate (5-7 year) Treasuries',
        'start_year': 2009,
        'early_replacement': 'VFITX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'bonds_treasury'
    },
    'VFITX': {
        'name': 'Intermediate (5-7 year) Treasuries Mutual Fund',  # duration: 5.2 years
        'start_year': 1991,
        'early_replacement': 'FGOVX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'bonds_treasury'
    },
    'FGOVX': {
        'name': 'Fidelity Goverment Income Fund',                   # duration: 5.5 years
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'bonds_treasury'
    },
    # '': {
    #     'name': '',
    #     'start_year': ,
    #     'early_replacement': '',
    #     'early_monthly_index_replacement': None,
    #     'suggest_in_search': False,
    #     'tax_category': ''
    # },

}
