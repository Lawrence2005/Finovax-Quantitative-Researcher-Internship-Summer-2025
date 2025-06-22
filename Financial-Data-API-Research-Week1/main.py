import pandas as pd
import requests

# Constants
Tiingo_API_TOKEN = "7f5ee704a8a6ebd637bbd4360b7f6cbd7418f706" # Replace with your own Tiingo API token
Alpha_Vantage_API_TOKEN = "GBMV74GZ3G8DGXO2" # Replace with your own Alpha Vantage API token

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
    request_url = (f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&resampleFreq=daily" if not end_date else \
                   f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&resampleFreq=daily") if frequency == 'daily' else \
                  (f"https://api.tiingo.com/iex/{ticker}/prices?startDate={start_date}&resampleFreq=1min&columns=open,high,low,close,volume" if not end_date else \
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

def fetch_alpha_vantage_date(ticker: str, frequency: str, start_date: str, end_date: str | None = None) -> pd.DataFrame:
    """
    Fetches financial data from Alpha Vantage API for a given ticker symbol and date range.
    
    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date if None
        frequency (str): Frequency of data ('daily' or 'intraday')

    Returns:
        pd.DataFrame: DataFrame with date-/datetime-indexed OHLCV(+adj_close) data
    """

    if frequency not in ['daily', 'intraday']:
        raise ValueError("Frequency must be either 'daily' or 'intraday'.")
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={Alpha_Vantage_API_TOKEN}'
    response = requests.get(url)

    # Extract time series data and set 'date' as the index
    result = pd.DataFrame(response.json()["Time Series (Daily)"]).T
    result.index = pd.to_datetime(result.index)

    # Ensure the DataFrame is sorted by date
    result = result.sort_index(ascending=False)

    # Filter by date range
    result = result[result.index >= start_date and (result.index <= end_date if end_date else True)]

    # Filter out OHLCV(+adj_close) columns
    cols = ['1. open', '2. high', '3. low', '4. close', '6. volume', '5. adjusted close'] if frequency == 'daily' else ['1. open', '2. high', '3. low', '4. close', '6. volume']
    result = result[cols]
    result.columns = ['open', 'high', 'low', 'close', 'volume', 'adjClose'] if frequency == 'daily' else ['open', 'high', 'low', 'close', 'volume']

    return result

def fetch_alpaca_data(ticker: str, frequency: str, start_date: str, end_date: str | None = None) -> pd.DataFrame:
    """
    Fetches financial data from Alpaca API for a given ticker symbol and date range.
    
    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date if None
        frequency (str): Frequency of data ('daily' or 'intraday')

    Returns:
        pd.DataFrame: DataFrame with date-/datetime-indexed OHLCV(+adj_close) data
    """
    raise NotImplementedError("Alpaca API integration is not implemented yet.")

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

    # if source != "tiingo":
    #     raise ValueError("Currently, only Tiingo source is supported.")
    
    if source == 'tiingo':
        result = fetch_tiingo_data(ticker, 'daily', start_date, end_date)
    elif source == 'alpha_vantage':
        result = fetch_alpha_vantage_date(ticker, 'daily', start_date, end_date)
    elif source == 'alpaca':
        result = fetch_alpaca_data(ticker, 'daily', start_date, end_date)
    else:
        raise ValueError("Unsupported source. Choose from 'tiingo', 'alpha_vantage', or 'alpaca'.")

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
    
    if source == 'tiingo':
        result = fetch_tiingo_data(ticker, 'intraday', start_date, end_date)
    elif source == 'alpha_vantage':
        result = fetch_alpha_vantage_date(ticker, 'intraday', start_date, end_date)
    elif source == 'alpaca':
        result = fetch_alpaca_data(ticker, 'intraday', start_date, end_date)
    else:
        raise ValueError("Unsupported source. Choose from 'tiingo', 'alpha_vantage', or 'alpaca'.")

    return result

if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    data = fetch_daily_data(ticker, start_date, end_date, source='alpha_vantage')
    print(data.head())