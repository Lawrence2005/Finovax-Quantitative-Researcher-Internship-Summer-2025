# Project Background and Significance:
Yahoo Finance, as a popular Python API source ("yfinance") for getting financial data, has recently gone through unstable breakdowns and updates these days, e.g. sometimes losing entire days of quotes or encountering rate-limit blocks. To safeguard our consistent and none-delayed data and analytical services, it’s critical to ***identify free, reliable, alternative data providers*** to replace Yahoo Finance when needed. While minute-level data remains a valuable goal, our current immediate priority is to ***secure daily historical price data*** (up through the latest trading date) from one or more alternative sources.

# Project Requirements:
**1. Research Daily-History Data Platforms**
- Identify and evaluate free or freemium Python-accessible APIs that deliver end-of-day OHLC(+adj_close) and volume data for U.S. equities.
- Consider factors such as data coverage (how far back and up-to-date), rate limits, ease of integration, documentation quality, and community support.
- Produce a shortlist (3-6) of candidates. Be sure to explore at least:
    - Alpha Vantage
    - Tiingo
    - IEX Cloud / iexfinance
    - Twelve Data
    - Google Finance
    - Polygon.io
- For each above, summarize the pros and cons—especially around free-tier limits and data freshness.

**2. Extend to Minute-Level (Optional/Bonus)**
- As an encouraged stretch goal, investigate which of your shortlisted providers (if any) also offer free 1-minute historical data (at least for the past/latest 5 trading days). Also research whether these 1-minute data sources (if any) are delayed or not.
- Note any additional setup or rate-limit considerations required to access intraday feeds.

# Deliverable:
A Python script (main.py) along with a .ipynb containing:
- A commented summary of your platform shortlist with pros/cons.
- A Python function that, given any U.S. ticker symbol (e.g. AAPL, TSLA), fetches the most recent daily OHLC(+adj_close) and volume data up to the latest trading date, along with a historical period of data required.
- (Optional) Notes or code snippets showing how you would fetch 1-minute data if available.
- Any necessary visualizations/plottings for demonstration purpose.