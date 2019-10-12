


TICKER_CONFIG = {

    'ONES': {
        'name': 'Ones',
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False
    },

    # U.S. Stock Market
    'VTI':  {
        'name': 'U.S. Stock Market',
        'start_year': 2001,
        'early_replacement': 'SPY',     # less broad market but good replacement
        'early_monthly_index_replacement': None,
        'suggest_in_search': True
    },
    'SPY': {
        'name': 'S&P 500',
        'start_year': 1993,
        'early_replacement': 'VFINX',   # the same, just mutual fund
        'early_monthly_index_replacement': None,
        'suggest_in_search': True
    },
    'VFINX': {
        'name': 'S&P 500 Mutual Fund',
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False
    },
    'QQQ': {
        'name': 'Nasdaq 100',
        'start_year': 1999,
        'early_replacement': 'RYOCX',   # the same, just mutual fund
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
    },
    'RYOCX': {
        'name': 'Nasdaq 100 Mutual Fund',
        'start_year': 1994,
        'early_replacement': 'ONES',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False
    },

    # Developed Markets
    'IEFA': {
        'name': 'Developed Stock Markets (EAFE)',
        'start_year': 2012,
        'early_replacement': 'EFA',
        'early_monthly_index_replacement': None,
        'suggest_in_search': True
    },
    'EFA': {
        'name': 'Developed Stock Markets (EAFE)',
        'start_year': 2001,
        'early_replacement': 'AAIEX',
        'early_monthly_index_replacement': None,
        'suggest_in_search': False
    },
    'AAIEX': {
        'name': 'American Beacon International Equity',
        'start_year': 1996,
        'early_replacement': 'OPPAX',   # pretty similar but not exact
        'early_monthly_index_replacement': None,
        'suggest_in_search': False
    },
    'OPPAX': {
        'name': 'Oppenheimer Global Fund', # caught up in dot com bubble
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False
    },

    # REITs
    'VNQ': {
        'name': 'U.S. Equities REITs',
        'start_year': 2004,
        'early_replacement': 'RWR',
        'early_monthly_index_replacement': 'eq_reit.csv',
        'suggest_in_search': True
    },
    'RWR': {
        'name': 'U.S. Equities REITs',
        'start_year': 2001,
        'early_replacement': 'DFREX',
        'early_monthly_index_replacement': 'eq_reit.csv',
        'suggest_in_search': False
    },
    'DFREX': {
        'name': 'DFA Real Estate Securities',
        'start_year': 1993,
        'early_replacement': None,
        'early_monthly_index_replacement': 'eq_reit.csv',
        'suggest_in_search': False
    },


    'VNQI': {
        'name': 'International Equities REITs',
        'start_year': 0000,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': True
    },

    'VMOT': {
        'name': 'Alpha Architect Value Momentum Trend',
        'start_year': 2017,
        'early_replacement': None,
        'early_monthly_index_replacement': 'eq_vmot.csv',
        'suggest_in_search': True
    },
    'QVAL': {
        'name': 'U.S. Quantitative Value',
        'start_year': 2014,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True
    },
    'IVAL': {
        'name': 'International Quantitative Value',
        'start_year': 2014,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True
    },
    'QMOM': {
        'name': 'U.S. Quantitative Momentum',
        'start_year': 2015,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True
    },
    'IMOM': {
        'name': 'International Quantitative Momentum',
        'start_year': 2015,
        'early_replacement': None,
        'early_monthly_index_replacement': 'alpha_architect.csv',
        'suggest_in_search': True
    },

    # '': {
    #     'name': '',
    #     'start_year': ,
    #     'early_replacement': '',
    #     'early_monthly_index_replacement': None,
    #     'suggest_in_search':
    # },

}
