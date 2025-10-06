import pandas as pd
import talib as ta
import pandas_ta as pta
import mplfinance as mpf
from yahoo_fin import stock_info as yf


class histData:
    # Class Constructor, with default values of parameters set to None
    def __init__(self, ticker=None, chosen_indicator_list=None, interval=None, start=None, end=None):
        # Class Variables assigned values either from parameters or manually setup
        self.chosen_indicator_list = chosen_indicator_list
        self.end = end
        self.start = start
        self.interval = interval
        self.ticker = ticker
        self.historical_data = pd.DataFrame()
        self.indicator_func_list = [
            self.get_Sma21,
            self.get_Sma34,
            self.get_SuperTrend,
            self.get_ATR,
            self.get_ADX,
            self.get_DMI
        ]
        self.parameter_name_list = ['SMA_21',
                                    'SMA_34',
                                    'Super Trend',
                                    'ATR',
                                    'ADX',
                                    'DMI']

    # Method gets historical data based on the given parameters, using Yahoo_fin
    def get_data(self):
        self.historical_data = yf.get_data(self.ticker, self.start, self.end, self.interval)
        # Dataframe columns renamed to work effectively with other modules
        self.historical_data.rename(
            columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"},
            inplace=True)

    # All get_* Methods below are responsible for calculating indicator values using talib or pandas_ta modules
    def get_Sma21(self):
        self.historical_data['SMA_21'] = ta.SMA(self.historical_data['Close'], timeperiod=21)

    def get_Sma34(self):
        self.historical_data['SMA_34'] = ta.SMA(self.historical_data['Close'], timeperiod=34)

    def get_ATR(self):
        self.historical_data['ATR'] = ta.ATR(self.historical_data['High'], self.historical_data['Low'],
                                             self.historical_data['Close'], timeperiod=14)

    def get_ADX(self):
        self.historical_data['ADX'] = ta.ADX(self.historical_data['High'], self.historical_data['Low'],
                                             self.historical_data['Close'], timeperiod=14)

    def get_DMI(self):
        self.historical_data['DIP'] = ta.PLUS_DI(self.historical_data['High'], self.historical_data['Low'],
                                                 self.historical_data['Close'], timeperiod=14)
        self.historical_data['DIM'] = ta.MINUS_DI(self.historical_data['High'], self.historical_data['Low'],
                                                  self.historical_data['Close'], timeperiod=14)

    def get_SuperTrend(self):
        super_temp = pta.supertrend(self.historical_data['High'], self.historical_data['Low'],
                                    self.historical_data['Close'],
                                    7, 3)
        self.historical_data['SUPERTl_7_3.0'] = super_temp['SUPERTl_7_3.0']
        self.historical_data['SUPERTs_7_3.0'] = super_temp['SUPERTs_7_3.0']

    # def get_BollingerBands(self):
    #     bb_temp = pta.bbands(self.historical_data['Close'], length=20, std=2)
    #     print(self.historical_data.columns.values)
    #     self.historical_data['BBL_20_2.0'] = bb_temp['BBL_20_2.0']
    #     self.historical_data['BBM_20_2.0'] = bb_temp['BBM_20_2.0']
    #     self.historical_data['BBU_20_2.0'] = bb_temp['BBU_20_2.0']
    #     self.historical_data['BBB_20_2.0'] = bb_temp['BBB_20_2.0']
    #     self.historical_data['BBP_20_2.0'] = bb_temp['BBP_20_2.0']

    # def get_MACD(self):
    #     macd_temp = pta.macd(self.historical_data['Close'], fast=12, slow=26, signal=9)
    #     self.historical_data['MACD_12_26_9'] = macd_temp['MACD_12_26_9']
    #     self.historical_data['MACDh_12_26_9'] = macd_temp['MACDh_12_26_9']
    #     self.historical_data['MACDs_12_26_9'] = macd_temp['MACDs_12_26_9']

    # Method calls each get_* method to calculate the indicators and add them to the historical_data DF
    def calc_indicators(self):
        for i in range(len(self.chosen_indicator_list)):
            self.indicator_func_list[i]()

    # Each graph_* method below returns a list which is responsible for adding that indicator to the graph when called
    def graph_sma21(self):
        return [mpf.make_addplot(self.historical_data['SMA_21'], color='magenta', panel=0)]

    def graph_sma34(self):
        return [mpf.make_addplot(self.historical_data['SMA_34'], color='yellow', panel=0)]

    def graph_ST(self):
        return [mpf.make_addplot(self.historical_data['SUPERTl_7_3.0'], color='green', panel=0),
                mpf.make_addplot(self.historical_data['SUPERTs_7_3.0'], color='red', panel=0)]

    # Some methods have a 'panel_num' param as they need to be placed in a separate subplot
    def graph_ATR(self, panel_num):
        return [mpf.make_addplot(self.historical_data['ATR'], color='black', panel=panel_num, ylabel='ATR')]

    def graph_ADX(self, panel_num):
        return [mpf.make_addplot(self.historical_data['ADX'], color='orange', panel=panel_num, ylabel='ADX')]

    def graph_DMI(self, panel_num):
        li = [mpf.make_addplot(self.historical_data['DIP'], color='green', panel=panel_num, ylabel='DMI'),
              mpf.make_addplot(self.historical_data['DIM'], color='red', panel=panel_num)]

        return li

    def graph_Bollinger(self):
        return [mpf.make_addplot(self.historical_data['BBL_20_2.0'], color='#ffa500', panel=0),
                mpf.make_addplot(self.historical_data['BBM_20_2.0'], color='#ffa500', panel=0),
                mpf.make_addplot(self.historical_data['BBU_20_2.0'], color='#ffa500', panel=0)]

    def graph_MACD(self, panel_num):
        li = [mpf.make_addplot(self.historical_data['MACD_12_26_9'], color='#0000ff', panel=panel_num, ylabel='MACD'),
              mpf.make_addplot(self.historical_data['MACDs_12_26_9'], color='#ffa500', panel=panel_num)]
        return li

    # Method is responsible for calling the graph_* methods and adding the indicators to the plot
    def plot_graph(self):
        """
        The for loop and nested if statements below are responsible for adding the indicators chosen by the user
        as well as incrementing panel numbers if an indicator is to have its own subplot
        """
        ind_plot = []
        count = 2
        for i in range(len(self.parameter_name_list)):
            if self.chosen_indicator_list[i] == 1:
                if self.parameter_name_list[i] == 'SMA_21':
                    ind_plot.extend(self.graph_sma21())
                    print("SMA21: " + str(count))
                elif self.parameter_name_list[i] == 'SMA_34':
                    ind_plot.extend(self.graph_sma34())
                    print("SMA34: " + str(count))
                elif self.parameter_name_list[i] == 'Super Trend':
                    ind_plot.extend(self.graph_ST())
                elif self.parameter_name_list[i] == 'Bollinger':
                    ind_plot.extend(self.graph_Bollinger())
                if i in [4, 5]:
                    if self.parameter_name_list[i] == 'ATR':
                        ind_plot.extend(self.graph_ATR(count))
                    elif self.parameter_name_list[i] == 'ADX':
                        ind_plot.extend(self.graph_ADX(count))
                        print("ADX: " + str(count))
                    # elif self.parameter_name_list[i] == 'DMI':
                    #     ind_plot.extend(self.graph_DMI(count))
                    # elif self.parameter_name_list[i] == 'MACD':
                    #     ind_plot.extend(self.graph_MACD(count))
                    #     print("MACD: "+ str(count))
                    count += 1

        s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6})  # making a style for the graph
        print(self.historical_data)

        # Making the graph itself using the ind_plot list of indicators and other params
        fig, axes = mpf.plot(
            self.historical_data,
            type='candle',
            returnfig=True,
            style=s,
            figsize=(15, 9),
            volume=True,
            figscale=8,
            addplot=ind_plot,
            panel_ratios=(5, 2),
            ylabel='Price (₹)'
        )

        # setting the graph title
        axes[0].set_title(self.ticker + ', ' + self.start + ' to ' + self.end, style='oblique',
                          fontsize=9, loc='center')

        return fig
