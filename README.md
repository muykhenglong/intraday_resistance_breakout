# Intraday Resistance Breakout Strategy

This repository contains a Python script designed to implement an intraday trading strategy based on resistance breakouts and volume surges, utilizing data from Yahoo Finance. The script automates the retrieval of stock data and the application of a technical analysis strategy to generate trading signals and calculate returns.

## Features

- **Automated Data Fetching**: Downloads intraday stock data using the `yfinance` library.
- **Technical Analysis**: Calculates Average True Range (ATR) and uses rolling maxima and minima to identify potential breakout points.
- **Trading Signals**: Generates buy and sell signals based on resistance breakouts combined with increased trading volume.
- **Performance Metrics**: Calculates key performance indicators such as Cumulative Annual Growth Rate (CAGR), Sharpe Ratio, and Maximum Drawdown.

## Requirements

- Python 3.8.19
- yfinance

Ensure you have the necessary Python packages installed: ```pip install yfinance```

## Strategy Description
### Signal Generation
Buy Signal: Generated when:
- The stock's high exceeds the rolling maximum close of the last 20 periods.
- Trading volume is more than 1.5 times the rolling maximum volume of the last 20 periods.

Sell Signal: Generated when:
- The stock's low drops below the rolling minimum close of the last 20 periods.
- Trading volume conditions are similar to the buy signal.

### Position Management
- Stop Loss for Buy: Triggered when the stock's low is below the previous close minus the calculated ATR.
- Stop Loss for Sell: Triggered when the stock's high is above the previous close plus the ATR.
- Switching Signals: Positions can switch from buy to sell or vice versa if opposing conditions are met during the holding period.

## How It Works

- Data Fetching: Downloads 5-minute interval stock price data for the tickers.
- Technical Calculations: Calculates Average True Range (ATR) over a 20-period window to gauge the stock's volatility and rolling maximums and minimums to identify breakout points.
- Signal Processing: Based on these criteria, buy or sell signals are generated. Position is at the breakout point and exits based on stop-loss conditions or if a contrary signal is detected.
- Performance Evaluation: Returns for each trade are calculated and aggregated to evaluate the overall performance of the strategy.

## Author

Muykheng Long - https://github.com/muykhenglong/
