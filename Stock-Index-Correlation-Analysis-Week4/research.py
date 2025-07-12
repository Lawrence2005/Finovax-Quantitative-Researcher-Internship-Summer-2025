# Import of required packages
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

# Definition of period of analysis
START_DATE = '2022-07-01'
END_DATE = '2025-07-11'

# Function to fetch stock data
def fetch_stock_data(index: str, start_date: str, end_date: str):
    """
    Fetch historical stock data for given between start_date and end_date.
    
    Parameters:
    index (str): Stock index ticker symbol ('DJIA' or 'NASDAQ-100').
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
    pd.DataFrame: DataFrame containing stock prices.
    """

    # Scrape the list of tickers from Wikipedia
    if index == 'DJIA':
        tickers = pd.read_html("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average")[2]['Symbol'].tolist()
        tickers.append('^DJI')  # Add the index itself
    elif index == 'NASDAQ-100':
        tickers = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]['Ticker'].tolist()
        tickers.append('^NDX')  # Add the index itself
    else:
        raise ValueError("Unsupported index. Use 'DJIA' or 'NASDAQ-100'.")

    # Fetch the data
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)

    return data['Close']

# Function to calculate daily returns
def calculate_daily_returns(prices: pd.DataFrame):
    """
    Calculate daily returns from stock prices.
    
    Parameters:
    prices (pd.DataFrame): DataFrame containing stock prices.
    
    Returns:
    pd.DataFrame: DataFrame containing daily returns.
    """

    return prices.pct_change().dropna()

# Function to calculate Pearson correlation coefficient
def calculate_pearson_correlation(returns: pd.DataFrame):
    """
    Calculate the Pearson correlation coefficient with respect to index for daily returns.
    
    Parameters:
    returns (pd.DataFrame): DataFrame containing daily returns.
    
    Returns:
    pd.DataFrame: DataFrame containing Pearson correlation coefficients.
    """

    return returns.iloc[:, :-1].corrwith(returns.iloc[:, -1]).dropna()

# Function to calculate rolling correlation
def calculate_rolling_correlation(returns: pd.DataFrame, window: int = 30):
    """
    Calculate rolling Pearson correlation coefficients for daily returns.
    
    Parameters:
    returns (pd.DataFrame): DataFrame containing daily returns.
    window (int): Window size for rolling correlation (default to 30).
    
    Returns:
    pd.DataFrame: DataFrame containing rolling correlation coefficients.
    """

    return returns.rolling(window=window).corr(returns.iloc[:, -1]).dropna()

# Function to filter stocks based on correlation threshold
def filter_stocks_by_correlation(correlation: pd.Series, threshold: float = 0.7):
    """
    Filter stocks based on a correlation threshold.
    
    Parameters:
    correlation (pd.Series): Series containing Pearson correlation coefficients.
    threshold (float): Correlation threshold for filtering (default to 0.7).
    
    Returns:
    pd.Series: Filtered Series of stocks with correlation above the threshold.
    """

    return correlation[correlation.abs() > threshold]

# Function for identifying stocks with high correlation to the index
def find_high_correlation_stocks(index: str, start_date: str, end_date: str, threshold: float = 0.7):
    """
    Identify stocks with high correlation to the specified index.
    
    Parameters:
    index (str): Stock index ticker symbol ('DJIA' or 'NASDAQ-100').
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.
    threshold (float): Correlation threshold for filtering (default to 0.7).
    
    Returns:
    pd.Series: Series of stocks with high correlation to the index.
    """

    stock_data = fetch_stock_data(index, start_date, end_date)

    daily_returns = calculate_daily_returns(stock_data)

    correlation = calculate_pearson_correlation(daily_returns)
    
    return filter_stocks_by_correlation(correlation, threshold)

# Function to show distribution of correlations 
def plot_correlation_distribution(correlations: pd.Series, index: str):
    """
    Plot the distribution of Pearson correlation coefficients for stocks with respect to the index.

    Parameters:
    correlations (pd.Series): Series containing Pearson correlation coefficients.
    index (str): Stock index ticker symbol ('DJIA' or 'NASDAQ-100').
    """

    # Set up the figure
    plt.figure(figsize=(8, 6))

    sns.histplot(correlations, kde=True, color='blue')

    plt.title(f"Distribution of Pearson Correlation Coefficients for {index} Stocks")
    plt.xlabel("Pearson Correlation")
    plt.ylabel("Number of Stocks")

    # Make y-axis show only integers
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.savefig(f"{index}_correlation_histogram.png")

# Function to plot scatter plot of correlations
def plot_correlation_scatter(correlations: pd.Series, returns: pd.DataFrame, index: str):
    """
    Plot scatter plot of stocks with respect to the index based on their daily returns.

    Parameters:
    correlations (pd.Series): Series containing Pearson correlation coefficients.
    returns (pd.DataFrame): DataFrame containing daily returns of stocks and index.
    index (str): Stock index ticker symbol ('DJIA' or 'NASDAQ-100').
    """

    # Select top 3 highly correlated stocks
    top_stocks = correlations.sort_values(ascending=False).head(3).index

    # Set up the figure
    plt.figure(figsize=(8, 6))

    # Plot all scatter plots in the same figure
    for stock in top_stocks:
        sns.scatterplot(
            x=returns['^DJI'] if index == 'DJIA' else returns['^NDX'], 
            y=returns[stock], 
            alpha=0.4, 
            label=f"{stock} (r = {correlations[stock]:.2f})"
        )

        # Regression line
        sns.regplot(
            x=returns['^DJI'] if index == 'DJIA' else returns['^NDX'], 
            y=returns[stock], 
            scatter=False,
            ci=None,  # hide confidence interval
            line_kws={'linestyle': '--'}  # optional: dashed line
        )

    # Add title and labels
    plt.title(f"Daily Return Scatter: Top 3 DJIA Stocks vs {index}")
    plt.xlabel(f"{index} Daily Return")
    plt.ylabel("Stock Daily Return")
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{index}_correlation_scatter.png")

for index in ['DJIA', 'NASDAQ-100']:
    # stocks = find_high_correlation_stocks('DJIA', START_DATE, END_DATE, 0.7)
    prices = fetch_stock_data(index, START_DATE, END_DATE)
    daily_returns = calculate_daily_returns(prices)
    correlation = calculate_pearson_correlation(daily_returns)
    plot_correlation_distribution(correlation, index)
    plot_correlation_scatter(correlation, daily_returns, index)

