## 🎯 Project Background and Significance
Finovax seeks to reinforce its risk-management toolkit by **building and rigorously evaluating a classic “all-weather” risk-parity portfolio**. Originally popularized by Ray Dalio’s Bridgewater Associates, this approach allocates capital across uncorrelated asset classes to perform robustly across economic regimes. By **replicating this strategy with liquid, low-cost ETFs** and then **subjecting it to extreme market events**, we can both validate our Python-based framework and deepen our understanding of portfolio resilience under stress.
- **Model Validation**: Ensures our portfolio construction code produces the expected risk-parity weights and performance.
- **Risk Insight**: Quantifies how an established risk-parity strategy behaves during historical crises (e.g., 2008 Global Financial Crisis, March 2020 COVID-19 sell-off, 2022 Russian-Ukraine War sell-off, 2025 Feb-April sell-off, etc.).
- **Process Maturity**: Lays groundwork for future stress-testing automation and integration into our systematic risk-monitoring platform.

## 📋 Project Requirements
1. Replication & Construction
- Select ETFs: Choose a representative set of ~5 ETFs covering equities, fixed income, commodities, inflation-linked bonds, and cash equivalents (e.g., SPY, TLT, GLD, TIP, BIL).
- Compute Risk Parity Weights:
    - Download daily price data (last 10 years) via a Python API (e.g., yfinance or another data provider).
    - Calculate rolling 126-day volatility for each ETF.
    - Invert volatilities and scale to sum to 100% to derive daily risk-parity weights.
- Backtest Performance:
    - Construct daily portfolio returns using those weights and total-return ETF series.
    - Compute annualized return, volatility, Sharpe ratio, and maximum drawdown over the full history.
2. Stress Testing Under Extreme Scenarios
- Define Scenarios: Select at least 3 historical stress periods, e.g.:
 a. 2007–2009 Global Financial Crisis (Oct 2007–Mar 2009)
 b. 2015–2016 Commodity Sell-off (Jul 2015–Feb 2016)
 c. March 2020 COVID-19 Crash (Feb–Apr 2020)
 d. 2022 Russian-Ukraine War sell-off
 e. 2025 Feb-April sell-off
- Scenario Analysis:
 a. Recompute portfolio performance metrics (cumulative return, peak drawdown, recovery time) for each stress window.
 b. Visualize equity-curve overlays for all scenarios alongside the full-history curve.
- Extreme-Shock Simulation (Optional Advanced):
 a. Apply hypothetical simultaneous shocks (e.g., –30% equity, +10% rates move, –15% commodity move) to the starting weights and estimate first-day portfolio loss.
 b. Compute both a full-history and a 252-day rolling Value-at-Risk (VaR) and Conditional VaR (CVaR) at 95% confidence based on historical daily returns.
3. Analysis & Recommendations
- Interpret Findings:
 a. Identify which stress period caused the largest drawdown and discuss why certain asset classes may have underperformed or outperformed.
 b. Evaluate whether the risk-parity weights adequately mitigated tail-risk in each case.
- Next Steps:
 Propose one enhancement to the framework (e.g., dynamic rebalancing frequency, inclusion of volatility targeting, use of alternative risk measures). Feel free to research existing academic research reports or industry papers to find related results & recommendations/enhancements

## 📦 Deliverable
- Deliverable 1: Jupyter notebook with clean, well-commented Python code and summary performance tables/plots (use Plotly for interactivity).
- Deliverable 3: A concise report (4–5 pages) summarizing methodology, stress-test results, key insights, and proposed enhancement. Include summary plots embedded from the notebook.