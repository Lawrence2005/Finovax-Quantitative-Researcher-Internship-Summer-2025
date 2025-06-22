import pandas as pd
import requests

# Constants
Tiingo_API_TOKEN = "7f5ee704a8a6ebd637bbd4360b7f6cbd7418f706" # Replace with your actual Tiingo API token

def fetch_tiingo_data(ticker: str, frequency: str, start_date: str, end_date: str | None = None) -> pd.DataFrame:
    """
    Fetches financial data from Tiingo API for a given ticker symbol and date range.

    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date if None
        frquency (str): Frequency of data ('daily' or 'intraday')

    Returns:
        pd.DataFrame: DataFrame with date-/datetime-indexed OHLCV(+adj_close) data
    """
    
    if frequency not in ['daily', 'intraday']:
        raise ValueError("Frequency must be either 'daily' or 'intraday'.")

    headers = {
        'Content-Type': 'application/json',
        'Authorization' : f'Token {Tiingo_API_TOKEN}'
    }
    request_url = (f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&resampleFreq=daily" if end_date is None else \
                   f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&resampleFreq=daily") if frequency == 'daily' else \
                  (f"https://api.tiingo.com/iex/{ticker}/prices?startDate={start_date}&resampleFreq=1min&columns=open,high,low,close,volume" if end_date is None else \
                   f"https://api.tiingo.com/iex/{ticker}/prices?startDate={start_date}&endDate={end_date}&resampleFreq=1min&columns=open,high,low,close,volume")
    requestResponse = requests.get(request_url, headers=headers)

    result = pd.DataFrame(requestResponse.json())

    # Parse 'date' and set it as the index
    result['date'] = pd.to_datetime(result['date'])
    result.set_index('date', inplace=True)
    if frequency == 'daily':
        result.index = result.index.date

    # Ensure the DataFrame is sorted by date
    result = result.sort_index(ascending=False)

    # Filter out OHLCV(+adj_close) columns
    cols = ['open', 'high', 'low', 'close', 'volume', 'adjClose'] if frequency == 'daily' else ['open', 'high', 'low', 'close', 'volume']
    result = result[cols]

    return result

def fetch_daily_data(ticker: str, start_date: str, end_date: str | None = None, source: str = 'tiingo') -> pd.DataFrame:
    """
    Given any U.S. ticker symbol (e.g. AAPL, TSLA), fetch daily OHLCV + adj_close data between start_date and end_date, inclusive.

    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date if None
        source (str): API source to use (e.g., 'tiingo', 'alpha_vantage')

    Returns:
        pd.DataFrame: DataFrame with date-indexed OHLCV(+adj_close) data
    """

    if source != "tiingo":
        raise ValueError("Currently, only Tiingo source is supported.")
    
    if source == 'tiingo':
        result = fetch_tiingo_data(ticker, 'daily', start_date, end_date)

    return result

def fetch_intraday_data(ticker: str, start_date: str, end_date: str | None = None, source: str = 'tiingo') -> pd.DataFrame:
    """
    Given any U.S. ticker symbol (e.g. AAPL, TSLA), fetch intraday OHLCV data between start_date and end_date, inclusive.
    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date if None
        source (str): API source to use (e.g., 'tiingo', 'alpha_vantage')

    Returns:
        pd.DataFrame: DataFrame with date-indexed intraday OHLCV data
    """
    
    if source != "tiingo":
        raise ValueError("Currently, only Tiingo source is supported.")
    
    if source == 'tiingo':
        result = fetch_tiingo_data(ticker, 'intraday', start_date, end_date)

    return result

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    data = fetch_daily_data(ticker, start_date, end_date, source='tiingo')
    print(data.head())