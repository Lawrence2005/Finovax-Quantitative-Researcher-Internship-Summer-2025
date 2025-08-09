## 🎯 Project Background and Significance
In the context of momentum-based trading strategies, identifying stocks that exhibit early signs of an uptrend breakout is a critical edge. Technical indicators—such as Donchian Channels, RSI, MACD, moving averages, and volume-based signals—serve as quantitative tools to detect these breakout patterns with consistency and speed. By integrating these indicators into an automated pipeline, we can screen a large set of equities and filter only those that meet our pre-defined conditions on any new trading day for a strong bullish momentum shift.\
This project applies this knowledge across a broader universe of stocks, namely the Nasdaq-100, in a systematic and actionable way. Please use technical indicators (or any form of variations of these indicators) to identify strong momentum stocks from a large pool. This proejct's results may significantly contribute to momentum strategy development processes.

## 📋 Project Requirements
**1. Data Acquisition**
- Download the pool of all Nasdaq 100 stocks using Python API from solid data sources like Yahoo Finance, and store them into a data folder.

**2. Stock Analysis**
- Use a certain indicator, or a variety of indicators, or their variations, to detect and find stocks on the latest day that break-out to form the uptrend. The code pipeline should be able to analyze and give latest results on a folder of Yahoo Finance's formats (Date, Open, High, Low, Close, Adj Close, Volume) of data up to the latest date, including multiple csv files

**3. Backtest**
- Prove the strategy can indeed identify the stocks' trend up-break by presenting statistical analysis and solid numbers (e.g. use numbers and data to prove that in history, after the stock meets a certain pattern/condition that the indicators present, the price of the stock indeed increases in the later days to a certain level). Please make sure these findings have solid statistical significance.


## 📦 Deliverable
A .ipynb file that contains the Python code pipeline with necessary visualizations and a PDF report of findings and research results/summaries.