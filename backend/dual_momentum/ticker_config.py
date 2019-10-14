


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
        'start_year': 2001,
        'early_replacement': 'SPY',     # less broad market but good replacement
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'SPY': {
        'name': 'S&P 500',
        'start_year': 1993,
        'early_replacement': 'VFINX',   # the same, just mutual fund
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'VFINX': {
        'name': 'S&P 500 Mutual Fund',
        'start_year': 1980,
        'early_replacement': None,
        'early_monthly_index_replacement': None,
        'suggest_in_search': False,
        'tax_category': 'equities'
    },
    'QQQ': {
        'name': 'Nasdaq 100',
        'start_year': 1999,
        'early_replacement': 'RYOCX',   # the same, just mutual fund
        'early_monthly_index_replacement': None,
        'suggest_in_search': True,
        'tax_category': 'equities'
    },
    'RYOCX': {
        'name': 'Nasdaq 100 Mutual Fund',
        'start_year': 1994,
        'early_replacement': 'ONES',
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
        'early_replacement': '',
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
