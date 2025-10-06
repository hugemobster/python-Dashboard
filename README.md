# python-Dashboard
This was my final project for cs50 called Nifty50. It is a python dashboard for the scripts within the nifty50 index

#### Video Demo:  https://youtu.be/-ukKVTXHyYg
#### Description:
- Made using python 3.8.10 (For all around python library stability)
- Libraries used:
    - TA-Lib: is a widely-used library in the world of technical analysis. It provides a wide range of functions for calculating various technical indicators such as moving averages, oscillators, volatility indicators, and trend-following indicators. In this program, TA-Lib is used to calculate indicators like Simple Moving Averages (SMA), Average True Range (ATR), Directional Movement Index (DMI), and Average Directional Index (ADX). These indicators are essential for analyzing stock trends and volatility, allowing users to perform technical analysis on stock price data.

    - pandas: is a versatile and widely used library for data manipulation and analysis. It provides data structures like DataFrames, which are essential for handling time-series data such as stock prices. In this program, pandas is used to store and manipulate historical stock data, including operations like renaming columns, adding calculated technical indicators, and organizing data for plotting. Pandas also enables the handling of large datasets and makes it easier to clean and preprocess data.

    - matplotlib: is a popular plotting library in Python, primarily used for generating static, interactive, and animated plots. While not directly used in the core functionality, it underpins mplfinance, which is used for creating candlestick charts. Matplotlib provides the flexibility to generate high-quality charts, customize them, and save them for further use. The program indirectly uses it through mplfinance for creating financial charts.

    - pandas_ta: is an extension of pandas that provides an easy interface to calculate various technical analysis indicators. While TA-Lib handles the core indicators, pandas_ta is used for additional indicators like Super Trend. This library seamlessly integrates with pandas DataFrames and makes it easy to calculate and add complex indicators to stock price data.

    - yahoo_fin: is a library for fetching financial data from Yahoo Finance. In this program, it is used to retrieve historical stock data based on a user-defined stock ticker, date range, and interval. The library supports various financial data types, such as historical stock prices, options data, and market statistics. It plays a crucial role in fetching the raw stock data, which is then used for analysis and visualization.

    - tkinter: is the standard Python library for building graphical user interfaces (GUIs). Tkinter is useful for creating a user interface where users can input stock tickers, select indicators, and customize chart settings. This would enhance the program's usability by allowing non-technical users to interact with it through buttons, dropdown menus, and other interactive elements.

    - mplfinance:  is a specialized library built on matplotlib that simplifies the creation of financial charts, especially candlestick charts. It is designed specifically for visualizing financial data such as stock prices, volume, and technical indicators. In this program, mplfinance is used to generate interactive candlestick charts, along with the ability to overlay additional indicators (like SMAs, ATR, Super Trend, etc.) on the same chart. The charts are highly customizable, allowing for tailored visual representations of stock data.

This program is designed to fetch, analyze, and visualize historical stock data, with the added functionality of displaying an industry-based stock dashboard. Initially, the program plots a dynamic dashboard showcasing the top 50 stocks from the nifty50 index, categorized into 13 industries. The dashboard provides the percent change of each stock from its previous close, allowing users to gauge market performance. This data can be refreshed to reflect real-time changes, providing an up-to-date view of stock movements across various sectors.

The histData class, which handles the retrieval of historical stock data. Users can specify a stock ticker, start and end dates, and an interval (e.g., daily or weekly), and the class fetches this data using the yahoo_fin package. The class then processes the stock data and calculates a variety of technical indicators, including Simple Moving Averages (SMA), Average True Range (ATR), Directional Movement Index (DMI), Average Directional Index (ADX), and Super Trend, using the talib and pandas_ta libraries. These indicators are essential for performing technical analysis and are added to the historical stock data for further analysis.

The plot_graph method is responsible for visualizing this data. It generates candlestick charts with the selected indicators, placing them on separate sub-panels for better readability. Users can choose which indicators they want to display, and the program automatically adjusts the layout and panel assignments. The visualizations are made interactive and informative, helping users to understand stock trends and make informed decisions.

Overall, the program provides a powerful platform for stock analysis, combining real-time market data, technical analysis indicators, and interactive visualizations. It is an excellent tool for traders and analysts seeking to analyze and track stock performance of the industries in the nifty50 index.
