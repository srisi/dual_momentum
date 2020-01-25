# Missing Tickers:
#
# elif ticker == "VFTAX":  # 2019
# stock = merge_ticker("VFTAX", "VFTSX")  # 2003
# elif ticker == "VFTSX":
# stock = merge_ticker("VFTSX", "VTI")
# elif ticker == "ESGV":  # 2018
# stock = merge_ticker("ESGV", "VFTSX")
#
# elif ticker == "VGLT":
# stock = merge_ticker("VGLT", "TLT")  # 2009
# elif ticker == "TLH":  # 2007                        Dur: 11.6 years
# stock = merge_ticker("TLH", "ONES")
#
# # U.S. Sectors
# elif ticker in ["XLV", "XLI", "XLE", "XLF", "XLU", "XLB", "XLP", "XLY", "XLK"]:
# stock = merge_ticker(ticker, "ONES")


TICKER_CONFIG = {

    "ONES": {
        "name": "Ones",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },

    "TBIL": {
        "name": "U.S Treasury Bills",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "bonds_treasury"
    },

    # U.S. Stock Market
    "VTI":  {
        "name": "U.S. Stock Market",
        "name_full": "Vanguard Total Stock Market Index Fund ETF",
        "start_year": 2001,
        "early_replacement": "SPY",     # less broad market but good replacement
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "SPY": {
        "name": "S&P 500",
        "name_full": "SPDR S&P 500 ETF ",
        "start_year": 1993,
        "early_replacement": "VFINX",   # the same, just mutual fund
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "VFINX": {
        "name": "S&P 500 Mutual Fund",
        "name_full": "Vanguard 500 Index Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "QQQ": {
        "name": "Nasdaq 100",
        "name_full": "Invesco QQQ Trust",
        "start_year": 1999,
        "early_replacement": "RYOCX",   # the same, just mutual fund
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "RYOCX": {
        "name": "Nasdaq 100 Mutual Fund",
        "name_full": "Rydex NASDAQ-100 Fund",
        "start_year": 1994,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },

    # U.S. ESG
    "ESGV": {
        "name": "U.S. ESG Stocks",
        "name_full": "Vanguard Environmental, Social and Governance U.S. Stock ETF",
        "start_year": 2018,
        "early_replacement": "VFTSX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "VFTSX": {
        "name": "Vanguard FTSE Social Index Fund",
        "start_year": 2000,
        "early_replacement": "VTI",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },



    # Developed Markets
    "IEFA": {
        "name": "Developed Stock Markets",
        "start_year": 2012,
        "early_replacement": "EFA",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "EFA": {
        "name": "Developed Stock Markets (EAFE)",
        "start_year": 2001,
        "early_replacement": "AAIEX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "AAIEX": {
        "name": "American Beacon International Equity",
        "start_year": 1996,
        "early_replacement": "OPPAX",   # pretty similar but not exact
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "OPPAX": {
        "name": "Oppenheimer Global Fund", # caught up in dot com bubble
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "VEA": {
        "name": "Developed Stock Markets",
        "name_full": "Vanguard FTSE Developed Markets Index Fund ETF",
        "start_year": 2007,
        "early_replacement": "EFA",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },

    # Developing Markets

    "IEMG": {
        "name": "Emerging Stock Markets",
        "name_full": "iShares Core MSCI Emerging Markets ETF",
        "start_year": 2012,
        "early_replacement": "EEM",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "EEM": {
        "name": "iShares MSCI Emerging Markets ETF",
        "start_year": 2003,
        "early_replacement": "TWMIX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "TWMIX": {
        "name": "American Century Emerging Markets Fund",
        "start_year": 1997,
        "early_replacement": "MADCX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "MADCX": {
        "name": "BlackRock Emerging Markets Fund, Inc.",
        "start_year": 1989,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "VWO": {
        "name": "Vanguard FTSE Emerging Markets Index Fund",
        "start_year": 2005,
        "early_replacement": "EEM",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },

    # Low Volatility

    "USMV": {
        "name": "U.S. Low Volatility Stocks",
        "name_full": "iShares Edge MSCI Min Vol USA ETF",
        "start_year": 2011,
        "early_replacement": "SPLV",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "SPLV": {
        "name": "iShares Edge MSCI Min Vol USA",
        "start_year": 2011,
        "early_replacement": "VTI",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },
    "EFAV": {
        "name": "Developed Markets Low Volatility Stocks",
        "name_full": "iShares Edge MSCI Min Vol EAFE ETF",
        "start_year": 2011,
        "early_replacement": "EFA",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "EEMV": {
        "name": "Developing Markets Low Volatility Stocks",
        "start_year": 2011,
        "early_replacement": "EEM",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },

    # Small Caps
    "VB": {
        "name": "U.S. Small Caps Stocks",
        "name_full": "Vanguard Small-Cap Index Fund ETF",
        "start_year": 2004,
        "early_replacement": "NAESX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "NAESX": {
        "name": "Vanguard Small Capitalization Index Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },

    "VSS": {
        "name": "All World ex-U.S. Small Caps Stocks",
        "name_full": "Vanguard Small Capitalization Index Fund",
        "start_year": 2009,
        "early_replacement": "VINEX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "VINEX": {
        "name": "Vanguard International Explorer Fund",
        "start_year": 1996,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "equities"
    },


    # REITs
    "VNQ": {
        "name": "U.S. Equity REITs",
        "start_year": 2004,
        "early_replacement": "RWR",
        "early_monthly_index_replacement": "eq_reit.csv",
        "suggest_in_search": True,
        "tax_category": "reits"
    },
    "RWR": {
        "name": "U.S. Equities REITs",
        "start_year": 2001,
        "early_replacement": "DFREX",
        "early_monthly_index_replacement": "eq_reit.csv",
        "suggest_in_search": False,
        "tax_category": "reits"
    },
    "DFREX": {
        "name": "DFA Real Estate Securities",
        "start_year": 1993,
        "early_replacement": None,
        "early_monthly_index_replacement": "eq_reit.csv",
        "suggest_in_search": False,
        "tax_category": "reits"
    },

    "VNQI": {
        "name": "International Equity REITs",
        "name_full": "Vanguard Global ex-US Real Estate Index Fund",
        "start_year": 2010,
        "early_replacement": "RWX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "reits"
    },
    "RWX": {
        "name": "SPDR Dow Jones International Real Estate ETF",
        "start_year": 2006,
        "early_replacement": "IERBX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "reits"
    },
    "IERBX": {
        "name": "Morgan Stanley International Fund, Inc. International Real Estate Portfolio",
        "start_year": 1997,
        "early_replacement": "EGLRX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "reits"
    },
    "EGLRX": {
        "name": "Aberdeen International Real Estate Equity Fund",
        "start_year": 1989,
        "early_replacement": "STMDX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "reits"
    },
    "STMDX": {
        "name": "Sterling Capital Stratton Real Estate Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "reits"
    },

    "REM": {
        "name": "U.S. Mortgage REITs",
        "name_full": "iShares Mortgage Real Estate Capped ETF",
        "start_year": 2007,
        "early_replacement": None,
        "early_monthly_index_replacement": "mortgage_reit.csv",
        "suggest_in_search": True,
        "tax_category": "reits"
    },

    # Alpha Architect

    # this merges the VMOT index backtest from alpha architect with a combo consisting of:
    # 50% VTI momentum and 50% IEFA momentum and IEF money market w/o taxes
    "VMOT": {
        "name": "Alpha Architect Value Momentum Trend",
        "start_year": 2017,
        "early_replacement": None,
        "early_monthly_index_replacement": "eq_vmot.csv",
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "QVAL": {
        "name": "U.S. Quantitative Value",
        "start_year": 2014,
        "early_replacement": None,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "IVAL": {
        "name": "International Quantitative Value",
        "start_year": 2014,
        "early_replacement": None,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "QMOM": {
        "name": "U.S. Quantitative Momentum",
        "start_year": 2015,
        "early_replacement": None,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": True,
        "tax_category": "equities"
    },
    "IMOM": {
        "name": "International Quantitative Momentum",
        "start_year": 2015,
        "early_replacement": None,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": True,
        "tax_category": "equities"
    },

    # Treasuries
    "VGIT": {
        "name": "U.S. Treasuries, 5-7 Years",
        "name_full": "Vanguard Intermediate-Term Treasury Fund ETF",
        "start_year": 2009,
        "early_replacement": "VFITX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 5,
        "tax_category": "bonds_treasury"
    },
    "VFITX": {
        "name": "Intermediate (5-7 year) Treasuries Mutual Fund",
        "start_year": 1991,
        "early_replacement": "FGOVX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 5,
        "tax_category": "bonds_treasury"
    },
    "FGOVX": {
        "name": "Fidelity Goverment Income Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 6,
        "tax_category": "bonds_treasury"
    },

    "IEF": {
        "name": "U.S. Treasuries, 7-10 Years",
        "start_year": 2002,
        "early_replacement": "VFITX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 8,
        "tax_category": "bonds_treasury"
    },

    "TLT": {
        "name": "U.S. Treasuries, 20+ Years",
        "name_full": "iShares 20+ Year Treasury Bond ETF",
        "start_year": 2002,
        "early_replacement": "VUSTX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 17,
        "tax_category": "bonds_treasury"
    },
    "VUSTX": {
        "name": "Vanguard Long Term Treasury Fund",
        "start_year": 1986,
        "early_replacement": "VWESX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 17,
        "tax_category": "bonds_treasury"
    },

    # duration 17 years. investment grade but similar reaction to interest rate changes
    "VWESX": {
        "name": "Vanguard Long Term Investment Grade Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "bonds_other"
    },

    # duration: 1.9 years
    "SHY": {
        "name": "U.S. Treasuries, 1-3 Year",
        "name_full": "iShares 1-3 Year Treasur Bond ETF",
        "start_year": 2003,
        "early_replacement": "TWUSX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 2,
        "tax_category": "bonds_treasury"
    },
    # duration 1.8 years
    "TWUSX": {
        "name": "American Century Short Term Government Fund",
        "start_year": 1982,
        "early_replacement": "FGOVX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "bonds_treasury"
    },

    "TIP": {
        "name": "U.S. Treasuries, Inflation Protected",
        "name_full": "iShares TIPS Bond ETF",
        "start_year": 2003,
        "early_replacement": "VIPSX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 7,
        "tax_category": "bonds_treasury"
    },
    "VIPSX": {
        "name": "Vanguard Inflation-Protected Securities Fund",
        "start_year": 2000,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 7,
        "tax_category": "bonds_treasury"
    },

    # Bonds, General

    "BOND": {
        "name": "PIMCO Active Bond ETF",
        "start_year": 2012,
        "early_replacement": "AGG",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 5,
        "tax_category": "bonds_other"
    },
    "BND": {
        "name": "Total U.S. Bond Market",
        "name_full": "Vanguard Total Bond Market ETF",
        "start_year": 2007,
        "early_replacement": "AGG",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 6,
        "tax_category": "bonds_other"
    },
    "AGG": {
        "name": "iShares Core U.S. Aggregate Bond ETF",
        "start_year": 2003,
        "early_replacement": "VBMFX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 6,
        "tax_category": "bonds_other"
    },
    "VBMFX": {
        "name": "Vanguard Total Bond Market Fund",
        "start_year": 1986,
        "early_replacement": "USAIX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 6,
        "tax_category": "bonds_other"
    },

    "USAIX": {
        "name": "USAA Income Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 6,
        "tax_category": "bonds_other"
    },

    # Bonds, US, Corporate

    "LQD": {
        "name": "U.S. Inv Grade Corporate Bonds",
        "name_full": "iShares iBoxx $ Investment Grade Corporate Bond ETF",
        "start_year": 2002,
        "early_replacement": "MFBFX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 9,
        "tax_category": "bonds_other"
    },
    "MFBFX": {
        "name": "MFS Corporate Bond Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 8,
        "tax_category": "bonds_other"
    },
    "VTC": {
        "name": "Vanguard Total Corporate Bond ETF",
        "start_year": 2017,
        "early_replacement": "LQD",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 8,
        "tax_category": "bonds_other"
    },

    "VCSH": {
        "name": "U.S. Inv Grade Short-Term Corporate Bonds",
        "name_full": "Vanguard Short-Term Corporate Bond Index Fund",
        "start_year": 2009,
        "early_replacement": "VFSTX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 3,
        "tax_category": "bonds_other"
    },
    "VFSTX": {
        "name": "Vanguard Short-Term Investment-Grade Fund",
        "start_year": 1983,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 2,
        "tax_category": "bonds_other"
    },


    # Bonds, US, High-Yield

    "HYG": {
        "name": "U.S. High Yield Corporate Bonds",
        "name_full": "iShares iBoxx $ High Yield Corporate Bond ETF",
        "start_year": 2007,
        "early_replacement": "SPHIX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 3,
        "tax_category": "bonds_other"
    },
    # NCINX high yield fund goes back to 1980 but starts at 2 cents and produces
    # absurd returns for high-yield debt in the the 1980s when it"s unlikely that
    # an investor would have actually owned high yield debt.
    "SPHIX": {
        "name": "Fidelity High Income Fund",
        "start_year": 1990,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 3,
        "tax_category": "bonds_other"
    },

    # Bonds, US, Muni

    "VTEB": {
        "name": "U.S. Municipal Bonds",
        "name_full": "Vanguard Tax-Exempt Bond Index Fund",
        "start_year": 2015,
        "early_replacement": "MUB",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 5,
        "tax_category": "bonds_muni"
    },
    "MUB": {
        "name": "iShares National Muni Bond ETF",
        "start_year": 2007,
        "early_replacement": "VWITX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 6,
        "tax_category": "bonds_muni"
    },
    "VWITX": {
        "name": "Vanguard Intermediate-Term Tax-Exempt Fund Investor Shares",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 5,
        "tax_category": "bonds_muni"
    },

    "HYD": {
        "name": "U.S. High-Yield Municipal Bonds",
        "name_full": "VanEck Vectors High-Yield Municipal Index ETF",
        "start_year": 2009,
        "early_replacement": "MMHYX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 7,
        "tax_category": "bonds_muni"
    },
    "MMHYX": {
        "name": "MFS Municipal High Income Fund",
        "start_year": 1984,
        "early_replacement": "PTAEX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 7,
        "tax_category": "bonds_muni"
    },
    "PTAEX": {
        "name": "Putnam Tax Exempt Income",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 7,
        "tax_category": "bonds_muni"
    },

    # Bonds, US, Mortgage-Backed

    "MBB": {
        "name": "U.S. Mortgage-Backed Securities",
        "name_full": "iShares MBS ETF",
        "start_year": 2007,
        "early_replacement": "OMBAX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 3,
        "tax_category": "bonds_other"
    },
    "OMBAX": {
        "name": "JPMorgan Mortgage-Backed Securities Fund",
        "start_year": 2000,
        "early_replacement": "FMSFX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 3,
        "tax_category": "bonds_other"
    },
    "FMSFX": {
        "name": "",
        "start_year": 1984,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 3,
        "tax_category": "bonds_other"
    },
    "VMBS": {
        "name": "Vanguard Mortgage-Backed Securities Index Fund",
        "start_year": 2009,
        "early_replacement": "MBB",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 4,
        "tax_category": "bonds_other"
    },

    # Bonds, US, Other

    "CWB": {
        "name": "U.S. Convertible Bonds",
        "start_year": 2009,
        "early_replacement": "PCONX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "bonds_other"
    },
    "PCONX": {
        "name": "Putnam Convertible Securities Fund",
        "start_year": 1980,
        "early_replacement": None,
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "tax_category": "bonds_other"
    },

    # International
    "BNDX": {
        "name": "Total International Bond Market",
        "start_year": 2013,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "tax_category": "bonds_other"
    },


    "PCY": {
        "name": "Emerging Markets Government Bonds",
        "name_full": "Invesco Emerging Markets Sovereign Debt ETF",
        "start_year": 2007,
        "early_replacement": "FNMIX",
        "early_monthly_index_replacement": None,
        "suggest_in_search": True,
        "duration": 10,
        "tax_category": "bonds_other"
    },
    "FNMIX": {
        "name": "Fidelity New Markets Income Fund",
        "start_year": 1993,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 6,
        "tax_category": "bonds_other"
    },
    "VWOB": {
        "name": "Vanguard Emerging Markets Government Bond Index Fund",
        "start_year": 2013,
        "early_replacement": "PCY",
        "early_monthly_index_replacement": None,
        "suggest_in_search": False,
        "duration": 8,
        "tax_category": "bonds_other"
    },

    # Commodities

    "GLD": {
        "name": "Gold",
        "name_full": "SPDR Gold Shares",
        "start_year": 2004,
        "early_replacement": None,
        "early_monthly_index_replacement": "gold_bullion.csv",
        "suggest_in_search": True,
        "tax_category": "collectibles"
    },
    # "": {
    #     "name": "",
    #     "start_year": ,
    #     "early_replacement": "",
    #     "early_monthly_index_replacement": None,
    #     "suggest_in_search": False,
    #     "duration": ,
    #     "tax_category": ""
    # },
    # "": {
    #     "name": "",
    #     "start_year": ,
    #     "early_replacement": "",
    #     "early_monthly_index_replacement": None,
    #     "suggest_in_search": False,
    #     "duration": ,
    #     "tax_category": ""
    # },
    # "": {
    #     "name": "",
    #     "start_year": ,
    #     "early_replacement": "",
    #     "early_monthly_index_replacement": None,
    #     "suggest_in_search": False,
    #     "duration": ,
    #     "tax_category": ""
    # },


}
