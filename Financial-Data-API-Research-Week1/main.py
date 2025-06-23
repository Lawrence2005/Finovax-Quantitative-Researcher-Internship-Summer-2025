import pandas as pd
import requests
from dotenv import load_dotenv
import os
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# Constants
Tiingo_API_TOKEN = "7f5ee704a8a6ebd637bbd4360b7f6cbd7418f706" # Replace with your own Tiingo API token
Alpha_Vantage_API_TOKEN = "GBMV74GZ3G8DGXO2" # Replace with your own Alpha Vantage API token
Alpaca_API_TOKEN = "PKBVL4VRUZ91Y4ZTTFKX" # Replace with your own Alpaca API token

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

    # Filter out OHLCV(+adj_close) columns
    cols = ['open', 'high', 'low', 'close', 'volume', 'adjClose'] if frequency == 'daily' else ['open', 'high', 'low', 'close', 'volume']
    result = result[cols]

    # Ensure the DataFrame is sorted by date
    result = result.sort_index(ascending=False)

    return result

def fetch_alpha_vantage_data(ticker: str, frequency: str, start_date: str, end_date: str | None = None) -> pd.DataFrame:
    """
    Fetches financial data from Alpha Vantage API for a given ticker symbol and date range.
    
    Parameters:
        ticker (str): U.S. equity ticker symbol (e.g., "AAPL")
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format, defaults to the most recent trading date if None
        frequency (str): Frequency of data ('daily' or 'intraday')

    Returns:
        pd.DataFrame: DataFrame with date-/datetime-indexed OHLCV data
    """

    if frequency not in ['daily', 'intraday']:
        raise ValueError("Frequency must be either 'daily' or 'intraday'.")
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={Alpha_Vantage_API_TOKEN}' if frequency == 'daily' else \
          (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={Alpha_Vantage_API_TOKEN}' if not end_date else \
           f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&month={end_date[:7]}&outputsize=full&apikey={Alpha_Vantage_API_TOKEN}')
    response = requests.get(url)

    # Extract time series data
    section = "Time Series (Daily)" if frequency == 'daily' else "Time Series (1min)"
    result = pd.DataFrame(response.json()[section]).T
    
    # Filter by date range
    if frequency == 'daily':
        mask = (result.index >= start_date) & ((result.index <= end_date) if end_date else True)
        result = result.loc[mask]

    # Filter out OHLCV, rename, and cast columns to appropriate types
    result = result[['1. open', '2. high', '3. low', '4. close', '5. volume']]
    result.columns = ['open', 'high', 'low', 'close', 'volume']
    result = result.astype({"open": float, "high": float, "low": float, "close": float, "volume": int})

    # Parse the index as datetime
    result.index = pd.to_datetime(result.index, utc = True)

    # Convert to datetime.date objects (drop time info if any)
    if frequency == 'daily':
        result.index = result.index.date

    # Name the index
    result.index.name = 'date'

    # Ensure the DataFrame is sorted by date
    result = result.sort_index(ascending=False)

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
    if frequency not in ['daily', 'intraday']:
        raise ValueError("Frequency must be either 'daily' or 'intraday'.")
    
    # Load Alpaca API secret from environment variables
    load_dotenv()
    SECRET = os.getenv("Alpaca_API_SECRET")
    
    client = StockHistoricalDataClient(Alpaca_API_TOKEN, SECRET)
    request_params_raw = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day if frequency == 'daily' else TimeFrame.Minute,
        start=datetime.strptime(start_date, '%Y-%m-%d'),
        end=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    )
    response_raw = client.get_stock_bars(request_params_raw)

    result = response_raw.df

    if frequency == 'daily':
        request_params_adj = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day if frequency == 'daily' else TimeFrame.Minute,
        start=datetime.strptime(start_date, '%Y-%m-%d'),
        end=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None,
        adjustment='all'
        )
        response_adj = client.get_stock_bars(request_params_adj)

        result['adjClose'] = response_adj.df['close']

    # Keep only the relevant columns and rename the index
    result = result.droplevel('symbol')
    cols = ['open', 'high', 'low', 'close', 'volume', 'adjClose'] if frequency == 'daily' else ['open', 'high', 'low', 'close', 'volume']
    result = result[cols]
    result.index = result.index.rename("date")

    # Parse the index as datetime (drop time info if any)
    if frequency == 'daily':
        result.index = result.index.date

    # Ensure the DataFrame is sorted by date
    result = result.sort_index(ascending=False)

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

    # if source != "tiingo":
    #     raise ValueError("Currently, only Tiingo source is supported.")
    
    if source == 'tiingo':
        result = fetch_tiingo_data(ticker, 'daily', start_date, end_date)
    elif source == 'alpha_vantage':
        result = fetch_alpha_vantage_data(ticker, 'daily', start_date, end_date)
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
        result = fetch_alpha_vantage_data(ticker, 'intraday', start_date, end_date)
    elif source == 'alpaca':
        result = fetch_alpaca_data(ticker, 'intraday', start_date, end_date)
    else:
        raise ValueError("Unsupported source. Choose from 'tiingo', 'alpha_vantage', or 'alpaca'.")

    return result