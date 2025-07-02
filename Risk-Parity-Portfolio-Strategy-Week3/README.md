## 🎯 Project Background and Significance
Finovax seeks to reinforce its risk-management toolkit by **building and rigorously evaluating a classic “all-weather” risk-parity portfolio**. Originally popularized by Ray Dalio’s Bridgewater Associates, this approach allocates capital across uncorrelated asset classes to perform robustly across economic regimes. By **replicating this strategy with liquid, low-cost ETFs** and then **subjecting it to extreme market events**, we can achieve:
- **Model Validation**: Ensures our Python-based portfolio construction framework produces the expected risk-parity weights and performance.
- **Risk Insight**: Quantifies how an established risk-parity strategy behaves during historical crises (e.g., 2008 Global Financial Crisis, March 2020 COVID-19 sell-off, 2022 Russian-Ukraine War sell-off, 2025 Feb-April sell-off, etc.) and deepens our understanding of portfolio resilience under stress.
- **Process Maturity**: Lays groundwork for future stress-testing automation and integration into our systematic risk-monitoring platform.

## 📋 Project Requirements
**1. Replicate & Construct**
- Select ETFs: Choose a representative set of ~5 ETFs covering equities, fixed income, commodities, inflation-linked bonds, and cash equivalents (e.g., SPY, TLT, GLD, TIP, BIL).
- Compute Risk Parity Weights:
    - Download daily price data (last 10 years) via a Python API (e.g., yfinance or another data provider).
    - Calculate rolling 126-day volatility for each ETF.
    - Invert volatilities and scale to sum to 100% to derive daily risk-parity weights.
- Backtest Performance:
    - Construct daily portfolio returns using those weights and total-return ETF series.
    - Compute annualized return, volatility, Sharpe ratio, and maximum drawdown over the full history.

**2. Stress Test Under Extreme Scenarios**
- Define Scenarios: Select at least 3 historical stress periods, e.g.:
    - 2007–2009 Global Financial Crisis (Oct 2007–Mar 2009)
    - 2015–2016 Commodity Sell-off (Jul 2015–Feb 2016)
    - March 2020 COVID-19 Crash (Feb–Apr 2020)
    - 2022 Russian-Ukraine War sell-off
    - 2025 Feb-April sell-off
- Scenario Analysis:
    - Recompute portfolio performance metrics (cumulative return, peak drawdown, recovery time) for each stress window.
    - Visualize equity-curve overlays for all scenarios alongside the full-history curve.
- Extreme-Shock Simulation (Optional Advanced):
    - Apply hypothetical simultaneous shocks (e.g., –30% equity, +10% rates move, –15% commodity move) to the starting weights and estimate first-day portfolio loss.
    - Compute both a full-history and a 252-day rolling Value-at-Risk (VaR) and Conditional VaR (CVaR) at 95% confidence based on historical daily returns.

**3. Analyze & Recommend**
- Interpret Findings:
    - Identify which stress period caused the largest drawdown and discuss why certain asset classes may have underperformed or outperformed.
    - Evaluate whether the risk-parity weights adequately mitigated tail-risk in each case.
- Next Steps:
Propose one enhancement to the framework (e.g., dynamic rebalancing frequency, inclusion of volatility targeting, use of alternative risk measures). Feel free to research existing academic research reports or industry papers to find related results & recommendations/enhancements

## 📦 Deliverable
A Jupyter notebook that:
- contains clean, well-commented Python 3.x code with clear modular functions and each code cell preceded by an explanatory markdown.
- shows summary performance tables/plots, preferrably in Plotly for interactivity
- employs pandas and numpy
- includes a single script or notebook cell that installs or imports all required packages to ensure reproducibility

and a report that:
- contains an executive summary, methodology, stress-test results, key insights, and proposed enhancement
- embeds summary plots, clearly labeled (axis titles, legends, scenario annotations), from the notebook
- is of 4–5 pages 