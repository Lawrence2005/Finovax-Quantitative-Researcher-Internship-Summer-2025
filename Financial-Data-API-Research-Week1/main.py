import pandas as pd

def fetch_daily_data(ticker: str, num_days: int, source: str = 'tiingo') -> pd.DataFrame:
    """
    Given any U.S. ticker symbol (e.g. AAPL, TSLA), fetch daily OHLCV + adj_close data for num_days up to the latest trading date.

    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        num_days (int): Length of historical data to fetch in days (e.g., 30 for the last 30 trading days)
        source (str): API source to use (e.g., 'tiingo', 'alpha_vantage')

    Returns:
        pd.DataFrame: DataFrame with date-indexed OHLCV(+adj_close) data
    """
    pass

# Entry point for quick testing
if __name__ == "__main__":
    df = fetch_daily_data("AAPL", "2023-01-01", "2023-12-31", source="tiingo")
    print(df.head())

# (Optional) Notes or code snippets showing how you would fetch 1-minute data if available.