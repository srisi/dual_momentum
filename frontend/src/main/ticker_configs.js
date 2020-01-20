


// export const ticker_configs = {
// "U.S. Stock Market": "VTI",
// "S&P 500": "SPY",
// "Nasdaq 100": "QQQ",
// "U.S. ESG Stocks": "ESGV",
// "Developed Stock Markets (EAFE)": "IEFA",
// "Emerging Stock Markets": "IEMG",
// "U.S. Low Volatility Stocks": "USMV",
// "Developed Markets Low Volatility Stocks": "EFAV",
// "Developing Markets Low Volatility Stocks": "EEMV",
// "U.S. Small Caps Stocks": "VB",
// "All World ex-U.S. Small Caps Stocks": "VSS",
// "U.S. Equities REITs": "VNQ",
// "International Equities REITs": "VNQI",
// "Alpha Architect Value Momentum Trend": "VMOT",
// "U.S. Quantitative Value": "QVAL",
// "International Quantitative Value": "IVAL",
// "U.S. Quantitative Momentum": "QMOM",
// "International Quantitative Momentum": "IMOM",
//
// "Intermediate (5-7 year) Treasuries": "VGIT",
// "7-10 Year Treasury Bonds": "IEF",
// "20+ Year Treasuries": "TLT",
// "1-3 Year Treasury Bond": "SHY"};




export const ticker_configs = {
    "ONES": {
        "name": "Ones",
        "start_year": 1980,
        "early_replacement": null,
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },

    "VTI":  {
        "name": "U.S. Stock Market",
        "name_full": "Vanguard Total Stock Market Index Fund ETF",
        "start_year": 2001,
        "early_replacement": "SPY",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "SPY": {
        "name": "S&P 500",
        "name_full": "SPDR S&P 500 ETF ",
        "start_year": 1993,
        "early_replacement": "VFINX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "VFINX": {
        "name": "S&P 500 Mutual Fund",
        "name_full": "Vanguard 500 Index Fund",
        "start_year": 1980,
        "early_replacement": null,
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "QQQ": {
        "name": "Nasdaq 100",
        "name_full": "Invesco QQQ Trust",
        "start_year": 1999,
        "early_replacement": "RYOCX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "RYOCX": {
        "name": "Nasdaq 100 Mutual Fund",
        "name_full": "Rydex NASDAQ-100 Fund",
        "start_year": 1994,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },


    "ESGV": {
        "name": "U.S. ESG Stocks",
        "name_full": "Vanguard Environmental, Social and Governance U.S. Stock ETF",
        "start_year": 2018,
        "early_replacement": "VFTSX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "VFTSX": {
        "name": "Vanguard FTSE Social Index Fund",
        "start_year": 2000,
        "early_replacement": "VTI",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },




    "IEFA": {
        "name": "Developed Stock Markets",
        "start_year": 2012,
        "early_replacement": "EFA",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "EFA": {
        "name": "Developed Stock Markets (EAFE)",
        "start_year": 2001,
        "early_replacement": "AAIEX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "AAIEX": {
        "name": "American Beacon International Equity",
        "start_year": 1996,
        "early_replacement": "OPPAX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "OPPAX": {
        "name": "Oppenheimer Global Fund",
        "start_year": 1980,
        "early_replacement": null,
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "VEA": {
        "name": "Developed Stock Markets",
        "name_full": "Vanguard FTSE Developed Markets Index Fund ETF",
        "start_year": 2007,
        "early_replacement": "EFA",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },



    "IEMG": {
        "name": "Emerging Stock Markets",
        "name_full": "iShares Core MSCI Emerging Markets ETF",
        "start_year": 2012,
        "early_replacement": "EEM",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "EEM": {
        "name": "iShares MSCI Emerging Markets ETF",
        "start_year": 2003,
        "early_replacement": "TWMIX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "TWMIX": {
        "name": "American Century Emerging Markets Fund",
        "start_year": 1997,
        "early_replacement": "MADCX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "MADCX": {
        "name": "BlackRock Emerging Markets Fund, Inc.",
        "start_year": 1989,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "VWO": {
        "name": "Vanguard FTSE Emerging Markets Index Fund",
        "start_year": 2005,
        "early_replacement": "EEM",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },



    "USMV": {
        "name": "U.S. Low Volatility Stocks",
        "name_full": "iShares Edge MSCI Min Vol USA ETF",
        "start_year": 2011,
        "early_replacement": "SPLV",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "SPLV": {
        "name": "iShares Edge MSCI Min Vol USA",
        "start_year": 2011,
        "early_replacement": "VTI",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },
    "EFAV": {
        "name": "Developed Markets Low Volatility Stocks",
        "name_full": "iShares Edge MSCI Min Vol EAFE ETF",
        "start_year": 2011,
        "early_replacement": "EFA",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "EEMV": {
        "name": "Developing Markets Low Volatility Stocks",
        "start_year": 2011,
        "early_replacement": "EEM",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },


    "VB": {
        "name": "U.S. Small Caps Stocks",
        "name_full": "Vanguard Small-Cap Index Fund ETF",
        "start_year": 2004,
        "early_replacement": "NAESX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "NAESX": {
        "name": "Vanguard Small Capitalization Index Fund",
        "start_year": 1980,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },

    "VSS": {
        "name": "All World ex-U.S. Small Caps Stocks",
        "name_full": "Vanguard Small Capitalization Index Fund",
        "start_year": 2009,
        "early_replacement": "VINEX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "VINEX": {
        "name": "Vanguard International Explorer Fund",
        "start_year": 1996,
        "early_replacement": "ONES",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "equities"
    },



    "VNQ": {
        "name": "U.S. Equities REITs",
        "start_year": 2004,
        "early_replacement": "RWR",
        "early_monthly_index_replacement": "eq_reit.csv",
        "suggest_in_search": true,
        "tax_category": "reits"
    },
    "RWR": {
        "name": "U.S. Equities REITs",
        "start_year": 2001,
        "early_replacement": "DFREX",
        "early_monthly_index_replacement": "eq_reit.csv",
        "suggest_in_search": false,
        "tax_category": "reits"
    },
    "DFREX": {
        "name": "DFA Real Estate Securities",
        "start_year": 1993,
        "early_replacement": null,
        "early_monthly_index_replacement": "eq_reit.csv",
        "suggest_in_search": false,
        "tax_category": "reits"
    },


    "VNQI": {
        "name": "International Equities REITs",
        "start_year": 1900,
        "early_replacement": null,
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "reits"
    },


    "VMOT": {
        "name": "Alpha Architect Value Momentum Trend",
        "start_year": 2017,
        "early_replacement": null,
        "early_monthly_index_replacement": "eq_vmot.csv",
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "QVAL": {
        "name": "U.S. Quantitative Value",
        "start_year": 2014,
        "early_replacement": null,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "IVAL": {
        "name": "International Quantitative Value",
        "start_year": 2014,
        "early_replacement": null,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "QMOM": {
        "name": "U.S. Quantitative Momentum",
        "start_year": 2015,
        "early_replacement": null,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": true,
        "tax_category": "equities"
    },
    "IMOM": {
        "name": "International Quantitative Momentum",
        "start_year": 2015,
        "early_replacement": null,
        "early_monthly_index_replacement": "alpha_architect.csv",
        "suggest_in_search": true,
        "tax_category": "equities"
    },


    "VGIT": {
        "name": "Intermediate (5-7 year) Treasuries",
        "start_year": 2009,
        "early_replacement": "VFITX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "bonds_treasury"
    },
    "VFITX": {
        "name": "Intermediate (5-7 year) Treasuries Mutual Fund",
        "start_year": 1991,
        "early_replacement": "FGOVX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "bonds_treasury"
    },
    "FGOVX": {
        "name": "Fidelity Goverment Income Fund",
        "start_year": 1980,
        "early_replacement": null,
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "bonds_treasury"
    },

    "IEF": {
        "name": "7-10 Year Treasury Bonds",
        "start_year": 2002,
        "early_replacement": "VFITX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "bonds_treasury"
    },

    "TLT": {
        "name": "20+ Year Treasuries",
        "name_full": "iShares 20+ Year Treasury Bond ETF",
        "start_year": 2002,
        "early_replacement": "VUSTX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "bonds_treasury"
    },
    "VUSTX": {
        "name": "Vanguard Long Term Treasury Fund",
        "start_year": 1986,
        "early_replacement": "VWESX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "bonds_treasury"
    },


    "VWESX": {
        "name": "Vanguard Long Term Investment Grade Fund",
        "start_year": 1980,
        "early_replacement": null,
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "bonds_other"
    },
    "SHY": {
        "name": "1-3 Year Treasury Bond",
        "start_year": 2003,
        "early_replacement": "TWUSX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": true,
        "tax_category": "bonds_treasury"
    },
    "TWUSX": {
        "name": "American Century Short Term Government Fund",
        "start_year": 1982,
        "early_replacement": "FGOVX",
        "early_monthly_index_replacement": null,
        "suggest_in_search": false,
        "tax_category": "bonds_treasury"
    }
};
