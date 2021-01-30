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
from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class TickerConfig:
    name: str
    name_full: str
    start_year: int
    early_replacement: Optional[str]
    early_monthly_index_replacement: Optional[Literal[
        'alpha_architect.csv', 'eq_reit.csv', 'eq_vmot.csv'
    ]]
    suggest_in_search: bool
    tax_category: Literal[
        'equities', 'reits', 'bonds_treasury', 'bonds_other', 'bonds_muni', 'collectibles'
    ]
    # tax_category: str
    duration: Optional[int]=None

TICKER_CONFIGS = {

    "ONES": TickerConfig(
        name="Ones",
        name_full="Ones",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),

    "TBIL": TickerConfig(
        name="U.S Treasury Bills",
        name_full="U.S Treasury Bills",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="bonds_treasury"
    ),

    # U.S. Stock Market
    "VTI": TickerConfig(
        name="U.S. Stock Market",
        name_full="Vanguard Total Stock Market Index Fund ETF",
        start_year=2001,
        early_replacement="SPY",     # less broad market but good replacement
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "SPY": TickerConfig(
        name="S&P 500",
        name_full="SPDR S&P 500 ETF ",
        start_year=1993,
        early_replacement="VFINX",   # the same, just mutual fund
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "VFINX": TickerConfig(
        name="S&P 500 Mutual Fund",
        name_full="Vanguard 500 Index Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "QQQ": TickerConfig(
        name="Nasdaq 100",
        name_full="Invesco QQQ Trust",
        start_year=1999,
        early_replacement="RYOCX",   # the same, just mutual fund
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "RYOCX": TickerConfig(
        name="Nasdaq 100 Mutual Fund",
        name_full="Rydex NASDAQ-100 Fund",
        start_year=1994,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),

    # U.S. ESG
    "ESGV": TickerConfig(
        name="U.S. ESG Stocks",
        name_full="Vanguard Environmental, Social and Governance U.S. Stock ETF",
        start_year=2018,
        early_replacement="VFTSX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "VFTSX": TickerConfig(
        name="Vanguard FTSE Social Index Fund",
        name_full="Vanguard FTSE Social Index Fund",
        start_year=2000,
        early_replacement="VTI",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),



    # Developed Markets
    "IEFA": TickerConfig(
        name="Developed Stock Markets",
        name_full="Developed Stock Markets",
        start_year=2012,
        early_replacement="EFA",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "EFA": TickerConfig(
        name="Developed Stock Markets (EAFE)",
        name_full="Developed Stock Markets (EAFE)",
        start_year=2001,
        early_replacement="AAIEX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "AAIEX": TickerConfig(
        name="American Beacon International Equity",
        name_full="American Beacon International Equity",
        start_year=1996,
        early_replacement="OPPAX",   # pretty similar but not exact
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "OPPAX": TickerConfig(
        name="Oppenheimer Global Fund", # caught up in dot com bubble
        name_full="Oppenheimer Global Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "VEA": TickerConfig(
        name="Developed Stock Markets",
        name_full="Vanguard FTSE Developed Markets Index Fund ETF",
        start_year=2007,
        early_replacement="EFA",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),

    # Developing Markets

    "IEMG": TickerConfig(
        name="Emerging Stock Markets",
        name_full="iShares Core MSCI Emerging Markets ETF",
        start_year=2012,
        early_replacement="EEM",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "EEM": TickerConfig(
        name="iShares MSCI Emerging Markets ETF",
        name_full="iShares MSCI Emerging Markets ETF",
        start_year=2003,
        early_replacement="TWMIX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "TWMIX": TickerConfig(
        name="American Century Emerging Markets Fund",
        name_full="American Century Emerging Markets Fund",
        start_year=1997,
        early_replacement="MADCX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "MADCX": TickerConfig(
        name="BlackRock Emerging Markets Fund, Inc.",
        name_full="BlackRock Emerging Markets Fund, Inc.",
        start_year=1989,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "VWO": TickerConfig(
        name="Vanguard FTSE Emerging Markets Index Fund",
        name_full="Vanguard FTSE Emerging Markets Index Fund",
        start_year=2005,
        early_replacement="EEM",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),

    # Low Volatility

    "USMV": TickerConfig(
        name="U.S. Low Volatility Stocks",
        name_full="iShares Edge MSCI Min Vol USA ETF",
        start_year=2011,
        early_replacement="SPLV",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "SPLV": TickerConfig(
        name="iShares Edge MSCI Min Vol USA",
        name_full="iShares Edge MSCI Min Vol USA",
        start_year=2011,
        early_replacement="VTI",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),
    "EFAV": TickerConfig(
        name="Developed Markets Low Volatility Stocks",
        name_full="iShares Edge MSCI Min Vol EAFE ETF",
        start_year=2011,
        early_replacement="EFA",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "EEMV": TickerConfig(
        name="Developing Markets Low Volatility Stocks",
        name_full="Developing Markets Low Volatility Stocks",
        start_year=2011,
        early_replacement="EEM",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),

    # Small Caps
    "VB": TickerConfig(
        name="U.S. Small Caps Stocks",
        name_full="Vanguard Small-Cap Index Fund ETF",
        start_year=2004,
        early_replacement="NAESX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "NAESX": TickerConfig(
        name="Vanguard Small Capitalization Index Fund",
        name_full="Vanguard Small Capitalization Index Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),

    "VSS": TickerConfig(
        name="All World ex-U.S. Small Caps Stocks",
        name_full="Vanguard Small Capitalization Index Fund",
        start_year=2009,
        early_replacement="VINEX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="equities"
    ),
    "VINEX": TickerConfig(
        name="Vanguard International Explorer Fund",
        name_full="Vanguard International Explorer Fund",
        start_year=1996,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="equities"
    ),


    # REITs
    "VNQ": TickerConfig(
        name="U.S. Equity REITs",
        name_full="U.S. Equity REITs",
        start_year=2004,
        early_replacement="RWR",
        early_monthly_index_replacement="eq_reit.csv",
        suggest_in_search=True,
        tax_category="reits"
    ),
    "RWR": TickerConfig(
        name="U.S. Equities REITs",
        name_full="U.S. Equities REITs",
        start_year=2001,
        early_replacement="DFREX",
        early_monthly_index_replacement="eq_reit.csv",
        suggest_in_search=False,
        tax_category="reits"
    ),
    "DFREX": TickerConfig(
        name="DFA Real Estate Securities",
        name_full="DFA Real Estate Securities",
        start_year=1993,
        early_replacement=None,
        early_monthly_index_replacement="eq_reit.csv",
        suggest_in_search=False,
        tax_category="reits"
    ),

    "VNQI": TickerConfig(
        name="International Equity REITs",
        name_full="Vanguard Global ex-US Real Estate Index Fund",
        start_year=2010,
        early_replacement="RWX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="reits"
    ),
    "RWX": TickerConfig(
        name="SPDR Dow Jones International Real Estate ETF",
        name_full="SPDR Dow Jones International Real Estate ETF",
        start_year=2006,
        early_replacement="IERBX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="reits"
    ),
    "IERBX": TickerConfig(
        name="Morgan Stanley International Fund, Inc. International Real Estate Portfolio",
        name_full="Morgan Stanley International Fund, Inc. International Real Estate Portfolio",
        start_year=1997,
        early_replacement="EGLRX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="reits"
    ),
    "EGLRX": TickerConfig(
        name="Aberdeen International Real Estate Equity Fund",
        name_full="Aberdeen International Real Estate Equity Fund",
        start_year=1989,
        early_replacement="STMDX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="reits"
    ),
    "STMDX": TickerConfig(
        name="Sterling Capital Stratton Real Estate Fund",
        name_full="Sterling Capital Stratton Real Estate Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="reits"
    ),

    "REM": TickerConfig(
        name="U.S. Mortgage REITs",
        name_full="iShares Mortgage Real Estate Capped ETF",
        start_year=2007,
        early_replacement=None,
        early_monthly_index_replacement="mortgage_reit.csv",
        suggest_in_search=True,
        tax_category="reits"
    ),

    # Alpha Architect

    # this merges the VMOT index backtest from alpha architect with a combo consisting of:
    # 50% VTI momentum and 50% IEFA momentum and IEF money market w/o taxes
    "VMOT": TickerConfig(
        name="Alpha Architect Value Momentum Trend",
        name_full="Alpha Architect Value Momentum Trend",
        start_year=2017,
        early_replacement=None,
        early_monthly_index_replacement="eq_vmot.csv",
        suggest_in_search=True,
        tax_category="equities"
    ),
    "QVAL": TickerConfig(
        name="U.S. Quantitative Value",
        name_full="U.S. Quantitative Value",
        start_year=2014,
        early_replacement=None,
        early_monthly_index_replacement="alpha_architect.csv",
        suggest_in_search=True,
        tax_category="equities"
    ),
    "IVAL": TickerConfig(
        name="International Quantitative Value",
        name_full="International Quantitative Value",
        start_year=2014,
        early_replacement=None,
        early_monthly_index_replacement="alpha_architect.csv",
        suggest_in_search=True,
        tax_category="equities"
    ),
    "QMOM": TickerConfig(
        name="U.S. Quantitative Momentum",
        name_full="U.S. Quantitative Momentum",
        start_year=2015,
        early_replacement=None,
        early_monthly_index_replacement="alpha_architect.csv",
        suggest_in_search=True,
        tax_category="equities"
    ),
    "IMOM": TickerConfig(
        name="International Quantitative Momentum",
        name_full="International Quantitative Momentum",
        start_year=2015,
        early_replacement=None,
        early_monthly_index_replacement="alpha_architect.csv",
        suggest_in_search=True,
        tax_category="equities"
    ),

    # Treasuries
    "VGIT": TickerConfig(
        name="U.S. Treasuries, 5-7 Years",
        name_full="Vanguard Intermediate-Term Treasury Fund ETF",
        start_year=2009,
        early_replacement="VFITX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=5,
        tax_category="bonds_treasury"
    ),
    "VFITX": TickerConfig(
        name="Intermediate (5-7 year) Treasuries Mutual Fund",
        name_full="Intermediate (5-7 year) Treasuries Mutual Fund",
        start_year=1991,
        early_replacement="FGOVX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=5,
        tax_category="bonds_treasury"
    ),
    "FGOVX": TickerConfig(
        name="Fidelity Goverment Income Fund",
        name_full="Fidelity Goverment Income Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=6,
        tax_category="bonds_treasury"
    ),

    "IEF": TickerConfig(
        name="U.S. Treasuries, 7-10 Years",
        name_full="U.S. Treasuries, 7-10 Years",
        start_year=2002,
        early_replacement="VFITX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=8,
        tax_category="bonds_treasury"
    ),

    "TLT": TickerConfig(
        name="U.S. Treasuries, 20+ Years",
        name_full="iShares 20+ Year Treasury Bond ETF",
        start_year=2002,
        early_replacement="VUSTX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=17,
        tax_category="bonds_treasury"
    ),
    "VUSTX": TickerConfig(
        name="Vanguard Long Term Treasury Fund",
        name_full="Vanguard Long Term Treasury Fund",
        start_year=1986,
        early_replacement="VWESX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=17,
        tax_category="bonds_treasury"
    ),

    # duration 17 years. investment grade but similar reaction to interest rate changes
    "VWESX": TickerConfig(
        name="Vanguard Long Term Investment Grade Fund",
        name_full="Vanguard Long Term Investment Grade Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="bonds_other"
    ),

    # duration: 1.9 years
    "SHY": TickerConfig(
        name="U.S. Treasuries, 1-3 Year",
        name_full="iShares 1-3 Year Treasur Bond ETF",
        start_year=2003,
        early_replacement="TWUSX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=2,
        tax_category="bonds_treasury"
    ),
    # duration 1.8 years
    "TWUSX": TickerConfig(
        name="American Century Short Term Government Fund",
        name_full="American Century Short Term Government Fund",
        start_year=1982,
        early_replacement="FGOVX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="bonds_treasury"
    ),

    "TIP": TickerConfig(
        name="U.S. Treasuries, Inflation Protected",
        name_full="iShares TIPS Bond ETF",
        start_year=2003,
        early_replacement="VIPSX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=7,
        tax_category="bonds_treasury"
    ),
    "VIPSX": TickerConfig(
        name="Vanguard Inflation-Protected Securities Fund",
        name_full="Vanguard Inflation-Protected Securities Fund",
        start_year=2000,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=7,
        tax_category="bonds_treasury"
    ),

    # Bonds, General

    "BOND": TickerConfig(
        name="PIMCO Active Bond ETF",
        name_full="PIMCO Active Bond ETF",
        start_year=2012,
        early_replacement="AGG",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=5,
        tax_category="bonds_other"
    ),
    "BND": TickerConfig(
        name="Total U.S. Bond Market",
        name_full="Vanguard Total Bond Market ETF",
        start_year=2007,
        early_replacement="AGG",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=6,
        tax_category="bonds_other"
    ),
    "AGG": TickerConfig(
        name="iShares Core U.S. Aggregate Bond ETF",
        name_full="iShares Core U.S. Aggregate Bond ETF",
        start_year=2003,
        early_replacement="VBMFX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=6,
        tax_category="bonds_other"
    ),
    "VBMFX": TickerConfig(
        name="Vanguard Total Bond Market Fund",
        name_full="Vanguard Total Bond Market Fund",
        start_year=1986,
        early_replacement="USAIX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=6,
        tax_category="bonds_other"
    ),

    "USAIX": TickerConfig(
        name="USAA Income Fund",
        name_full="USAA Income Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=6,
        tax_category="bonds_other"
    ),

    # Bonds, US, Corporate

    "LQD": TickerConfig(
        name="U.S. Inv Grade Corporate Bonds",
        name_full="iShares iBoxx $ Investment Grade Corporate Bond ETF",
        start_year=2002,
        early_replacement="MFBFX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=9,
        tax_category="bonds_other"
    ),
    "MFBFX": TickerConfig(
        name="MFS Corporate Bond Fund",
        name_full="MFS Corporate Bond Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=8,
        tax_category="bonds_other"
    ),
    "VTC": TickerConfig(
        name="Vanguard Total Corporate Bond ETF",
        name_full="Vanguard Total Corporate Bond ETF",
        start_year=2017,
        early_replacement="LQD",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=8,
        tax_category="bonds_other"
    ),

    "VCSH": TickerConfig(
        name="U.S. Inv Grade Short-Term Corporate Bonds",
        name_full="Vanguard Short-Term Corporate Bond Index Fund",
        start_year=2009,
        early_replacement="VFSTX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=3,
        tax_category="bonds_other"
    ),
    "VFSTX": TickerConfig(
        name="Vanguard Short-Term Investment-Grade Fund",
        name_full="Vanguard Short-Term Investment-Grade Fund",
        start_year=1983,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=2,
        tax_category="bonds_other"
    ),


    # Bonds, US, High-Yield

    "HYG": TickerConfig(
        name="U.S. High Yield Corporate Bonds",
        name_full="iShares iBoxx $ High Yield Corporate Bond ETF",
        start_year=2007,
        early_replacement="SPHIX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=3,
        tax_category="bonds_other"
    ),
    # NCINX high yield fund goes back to 1980 but starts at 2 cents and produces
    # absurd returns for high-yield debt in the the 1980s when it"s unlikely that
    # an investor would have actually owned high yield debt.
    "SPHIX": TickerConfig(
        name="Fidelity High Income Fund",
        name_full="Fidelity High Income Fund",
        start_year=1990,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=3,
        tax_category="bonds_other"
    ),

    # Bonds, US, Muni

    "VTEB": TickerConfig(
        name="U.S. Municipal Bonds",
        name_full="Vanguard Tax-Exempt Bond Index Fund",
        start_year=2015,
        early_replacement="MUB",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=5,
        tax_category="bonds_muni"
    ),
    "MUB": TickerConfig(
        name="iShares National Muni Bond ETF",
        name_full="iShares National Muni Bond ETF",
        start_year=2007,
        early_replacement="VWITX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=6,
        tax_category="bonds_muni"
    ),
    "VWITX": TickerConfig(
        name="Vanguard Intermediate-Term Tax-Exempt Fund Investor Shares",
        name_full="Vanguard Intermediate-Term Tax-Exempt Fund Investor Shares",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=5,
        tax_category="bonds_muni"
    ),

    "HYD": TickerConfig(
        name="U.S. High-Yield Municipal Bonds",
        name_full="VanEck Vectors High-Yield Municipal Index ETF",
        start_year=2009,
        early_replacement="MMHYX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=7,
        tax_category="bonds_muni"
    ),
    "MMHYX": TickerConfig(
        name="MFS Municipal High Income Fund",
        name_full="MFS Municipal High Income Fund",
        start_year=1984,
        early_replacement="PTAEX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=7,
        tax_category="bonds_muni"
    ),
    "PTAEX": TickerConfig(
        name="Putnam Tax Exempt Income",
        name_full="Putnam Tax Exempt Income",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=7,
        tax_category="bonds_muni"
    ),

    # Bonds, US, Mortgage-Backed

    "MBB": TickerConfig(
        name="U.S. Mortgage-Backed Securities",
        name_full="iShares MBS ETF",
        start_year=2007,
        early_replacement="OMBAX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=3,
        tax_category="bonds_other"
    ),
    "OMBAX": TickerConfig(
        name="JPMorgan Mortgage-Backed Securities Fund",
        name_full="JPMorgan Mortgage-Backed Securities Fund",
        start_year=2000,
        early_replacement="FMSFX",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=3,
        tax_category="bonds_other"
    ),
    "FMSFX": TickerConfig(
        name="Fidelity Mortgage Securities Fund",
        name_full="Fidelity Mortgage Securities Fund",
        start_year=1984,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=3,
        tax_category="bonds_other"
    ),
    "VMBS": TickerConfig(
        name="Vanguard Mortgage-Backed Securities Index Fund",
        name_full="Vanguard Mortgage-Backed Securities Index Fund",
        start_year=2009,
        early_replacement="MBB",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=4,
        tax_category="bonds_other"
    ),

    # Bonds, US, Other

    "CWB": TickerConfig(
        name="U.S. Convertible Bonds",
        name_full="U.S. Convertible Bonds",
        start_year=2009,
        early_replacement="PCONX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="bonds_other"
    ),
    "PCONX": TickerConfig(
        name="Putnam Convertible Securities Fund",
        name_full="Putnam Convertible Securities Fund",
        start_year=1980,
        early_replacement=None,
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        tax_category="bonds_other"
    ),

    # International
    "BNDX": TickerConfig(
        name="Total International Bond Market",
        name_full="Total International Bond Market",
        start_year=2013,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        tax_category="bonds_other"
    ),


    "PCY": TickerConfig(
        name="Emerging Markets Government Bonds",
        name_full="Invesco Emerging Markets Sovereign Debt ETF",
        start_year=2007,
        early_replacement="FNMIX",
        early_monthly_index_replacement=None,
        suggest_in_search=True,
        duration=10,
        tax_category="bonds_other"
    ),
    "FNMIX": TickerConfig(
        name="Fidelity New Markets Income Fund",
        name_full="Fidelity New Markets Income Fund",
        start_year=1993,
        early_replacement="ONES",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=6,
        tax_category="bonds_other"
    ),
    "VWOB": TickerConfig(
        name="Vanguard Emerging Markets Government Bond Index Fund",
        name_full="Vanguard Emerging Markets Government Bond Index Fund",
        start_year=2013,
        early_replacement="PCY",
        early_monthly_index_replacement=None,
        suggest_in_search=False,
        duration=8,
        tax_category="bonds_other"
    ),

    # Commodities

    "GLD": TickerConfig(
        name="Gold",
        name_full="SPDR Gold Shares",
        start_year=2004,
        early_replacement=None,
        early_monthly_index_replacement="gold_bullion.csv",
        suggest_in_search=True,
        tax_category="collectibles"
    )
}
