import pandas as pd
import pandas_market_calendars as mcal
import requests

# Constants
Tiingo_API_TOKEN = "7f5ee704a8a6ebd637bbd4360b7f6cbd7418f706" # Replace with your actual Tiingo API token

def get_most_recent_trading_date() -> str:
    """
    Get the most recent trading date for the NYSE.
    Returns:
        pd.Timestamp: The most recent trading date.
    """

    # Define the NYSE calendar and get the current time in NY timezone
    nyse = mcal.get_calendar('NYSE')
    now = pd.Timestamp.now(tz='America/New_York')

    # Get the last trading schedule
    schedule = nyse.schedule(start_date=now - pd.Timedelta(days=7), end_date=now)
    last_open_day = schedule.index.max()

    return last_open_day.strftime('%Y-%m-%d')

def fetch_daily_data(ticker: str, start_date: str, end_date: str = get_most_recent_trading_date(), source: str = 'tiingo') -> pd.DataFrame:
    """
    Given any U.S. ticker symbol (e.g. AAPL, TSLA), fetch daily OHLCV + adj_close data for num_days days up to the latest trading date.

    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date
        source (str): API source to use (e.g., 'tiingo', 'alpha_vantage')

    Returns:
        pd.DataFrame: DataFrame with date-indexed OHLCV(+adj_close) data
    """

    if source != "tiingo":
        raise ValueError("Currently, only Tiingo source is supported.")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : f'Token {Tiingo_API_TOKEN}'
    }
    requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&format=csv&resampleFreq=monthly", 
                                   headers=headers)
    
    result = pd.DataFrame(requestResponse.json())

    # Parse 'date' and set it as the index
    result['date'] = pd.to_datetime(result['date'])
    result.set_index('date', inplace=True)

    # Ensure the DataFrame is sorted by date
    result = result.sort_index(ascending=True)

    # Filter out OHLCV + adj_close columns
    result = result[['open', 'high', 'low', 'close', 'volume', 'adjClose']]

    return result

# Entry point for quick testing
if __name__ == "__main__":
    df = fetch_daily_data("AAPL", 5, source="tiingo")
    print(df.head())

# (Optional) Notes or code snippets showing how you would fetch 1-minute data.