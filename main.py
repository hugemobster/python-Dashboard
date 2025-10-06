import time
from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from yahoo_fin import stock_info as yf
from datetime import date
import datetime
from histData import histData
from ScrollFrame import DoubleScrolledFrame
import threading


# Class inherits TopLevel which is a
# callable window and acts as a container
class HistDataPane(Toplevel):
    # Class Constructor Method, with default values set to None
    def __init__(self, master=None, fullMarketDf=None):
        super().__init__(master=master)
        self.title("Historical Data")  # setting window title
        self.geometry("1000x1100")  # Setting window size

        # creating attributes and assigning values
        self.fullMarkDf = fullMarketDf
        self.chosen_ticker = None
        self.chosen_interval = None
        self.chosen_start = None
        self.chosen_end = None
        self.chosen_indicators = None
        self.historical_graph = None

        # Creating the main, toolbar and data input containers
        self.main_container = ttk.Frame(self, relief='groove', borderwidth=2)
        self.main_container.place(relx=0, rely=0, relheight=0.96, relwidth=0.75)
        self.toolbar_container = ttk.Frame(self, relief='groove', borderwidth=2)
        self.toolbar_container.place(relx=0, rely=0.96, relheight=0.04, relwidth=0.75)
        self.hist_data_cont = ttk.Frame(self, relief='groove', borderwidth=2)
        self.hist_data_cont.place(relx=0.75, rely=0, relheight=1, relwidth=0.25)

        self.script_prompt = ttk.Label(self.hist_data_cont, text="Choose a script:")  # Label prompt
        self.script_prompt.pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))

        # Making dropdown box for choosing a script
        self.script_option = tk.StringVar(self, 1)
        self.hist_option_box = ttk.Combobox(self.hist_data_cont, textvariable=self.script_option,
                                            values=tuple(self.fullMarkDf['Symbol'].values), state='readonly')
        self.hist_option_box.pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.hist_option_box.current(1)

        # Label prompt
        self.ind_prompt = ttk.Label(self.hist_data_cont,
                                    text='Choose Your Indicators:').pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))

        # Making a multiple choice, section for choosing graphical indicators as per client requirements
        self.indicator_checks = [IntVar() for i in range(6)]
        self.sma21 = Checkbutton(self.hist_data_cont, text="SMA_21",
                                 variable=self.indicator_checks[0]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.sma34 = Checkbutton(self.hist_data_cont, text="SMA_34",
                                 variable=self.indicator_checks[1]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.superT = Checkbutton(self.hist_data_cont, text="Super Trend",
                                  variable=self.indicator_checks[2]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.ATR = Checkbutton(self.hist_data_cont, text="ATR",
                               variable=self.indicator_checks[3]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.ADX = Checkbutton(self.hist_data_cont, text="ADX",
                               variable=self.indicator_checks[4]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.DMI = Checkbutton(self.hist_data_cont, text="DMI",
                               variable=self.indicator_checks[5]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        # self.Boll = Checkbutton(self.hist_data_cont, text="Bollinger Band",
        #                         variable=self.indicator_checks[6]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        # self.MACD = Checkbutton(self.hist_data_cont, text="MACD",
        #                         variable=self.indicator_checks[7]).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))

        # Label prompt
        self.date_prompt = ttk.Label(self.hist_data_cont,
                                     text="Choose start and end date below\n(MM/DD/YYYY):").pack(side=TOP, anchor=W,
                                                                                                 padx=(5, 5),
                                                                                                 pady=(5, 5))
        # Starting and end date inputs, as date entry
        self.l1 = ttk.Label(self.hist_data_cont,
                            text="Start date:").pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.startDateVar = tk.StringVar()
        self.startDateEntry = DateEntry(self.hist_data_cont, selectmode='day',
                                        textvariable=self.startDateVar)
        self.startDateEntry.set_date(datetime.datetime.today() - datetime.timedelta(days=1))

        self.startDateEntry.pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.l2 = ttk.Label(self.hist_data_cont,
                            text="End date:").pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))
        self.endDateVar = tk.StringVar()
        self.endDateEntry = DateEntry(self.hist_data_cont, selectmode='day',
                                      textvariable=self.endDateVar).pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))

        self.interval_prompt = tk.Label(self.hist_data_cont,
                                        text='Choose a time interval \n'
                                             '(default is 1 day):').pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))

        # Time interval of data, input given as radio button
        self.interval_var = tk.IntVar(master=self.hist_data_cont, value=1)
        self.day_inter = Radiobutton(self.hist_data_cont, text="1 day",
                                     variable=self.interval_var, value=1).pack(side=TOP, anchor=W, padx=(5, 5),
                                                                               pady=(5, 5))
        self.week_inter = Radiobutton(self.hist_data_cont, text="1 week",
                                      variable=self.interval_var, value=2).pack(side=TOP, anchor=W, padx=(5, 5),
                                                                                pady=(5, 5))
        self.month_inter = Radiobutton(self.hist_data_cont, text="1 month",
                                       variable=self.interval_var, value=3).pack(side=TOP, anchor=W, padx=(5, 5),
                                                                                 pady=(5, 5))
        self.minute_inter = Radiobutton(self.hist_data_cont, text="1 minute",
                                        variable=self.interval_var, value=4).pack(side=TOP, anchor=W, padx=(5, 5),
                                                                                  pady=(5, 5))

        # Button to make the graph itself, calls historical_data_plotter()
        self.make_graph_btn = tk.Button(self.hist_data_cont, text='Make Graph',
                                        command=lambda: self.historical_data_plotter())
        self.make_graph_btn.pack(side=TOP, anchor=W, padx=(5, 5), pady=(5, 5))

    # Method returns historical data graph with indicators
    def historical_data_getter(self):
        # Object of histData class, used to make the historical graph and indicators. Parameters taken from user input
        h1 = histData(ticker=self.chosen_ticker,
                      chosen_indicator_list=self.chosen_indicators,
                      interval=self.chosen_interval,
                      start=self.chosen_start,
                      end=self.chosen_end)
        h1.get_data()
        h1.calc_indicators()
        return h1.plot_graph()

    # Method is used to display the historical data graph based on user input
    def historical_data_plotter(self):
        # Called to organise data as needed
        self.setValues()

        try:
            self.historical_graph.get_tk_widget().forget()  # Removes any previous plots if there are any
        except:
            pass

        # Creates the canvas with historical graph in it
        self.historical_graph = FigureCanvasTkAgg(self.historical_data_getter(), master=self.main_container)
        self.historical_graph.draw()
        self.historical_graph.get_tk_widget().pack()

        try:
            for item in self.toolbar_container.winfo_children():  # Used to remove any children from the container
                item.destroy()
        except:
            pass

        toolbar = NavigationToolbar2Tk(self.historical_graph, self.toolbar_container)  # Creating the toolbar itself
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.historical_graph.get_tk_widget().pack()  # Packing the canvas into the container

    # Method is used to call all values taken by the user
    def setValues(self):
        self.chosen_ticker = str(self.script_option.get())
        self.chosen_indicators = [i.get() for i in self.indicator_checks]
        self.chosen_interval = self.interval_var.get()
        self.chosen_start = str(self.startDateVar.get())
        self.chosen_end = str(self.endDateVar.get())


# Class inherits tkinter.Tk(),
# thereby becoming the root window of the application
class MainPage(tk.Tk):
    # Constructor Method below
    def __init__(self):
        super().__init__()

        messagebox.askyesno(title='App is launching', message='The app will take a few seconds to load, you will be '
                                                              'presented with data of each script since last close as '
                                                              'a percentage')

        # Initializing Canvas Variables
        self.c0 = None
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.c5 = None
        self.c6 = None
        self.c7 = None
        self.c8 = None
        self.c9 = None
        self.c10 = None
        self.c11 = None
        self.c12 = None
        self.c13 = None

        # Importing all stock scripts & symbols
        self.full_market_df = pd.read_csv('ind_nifty50list.csv')
        self.full_market_df = self.full_market_df.drop(['Series', 'ISIN Code'], axis=1)
        self.full_market_df['Symbol'] = self.full_market_df['Symbol'].astype(str) + '.NS'
        self.industryList = self.full_market_df['Industry'].unique()

        # Creating Array of Dataframes, for each industry in the market
        self.stock_sect_arr = [pd.DataFrame() for _ in range(len(self.industryList))]

        # Calling the make_gui() function to setup the GUI
        self.make_gui()

        print('starting prev close')
        self.prev_close()
        print('got prev close, setting tickers')
        self.set_tickers()
        print('tickers set, calculating percent')
        self.calc_percent()
        print('percent calculated, plotting now')
        self.plot_data()

    def make_gui(self):
        # Setting the root window settings; size, resizable or not, etc
        self.title('Stock Data')
        self.state('zoomed')
        self.resizable(True, True)

        # Menu Container at the top of window, holds info label and buttons
        self.menu_frame = ttk.Frame(self, relief='groove', borderwidth=2)
        self.menu_frame.place(relx=0.0, rely=0.0, relheight=0.05, relwidth=1)

        # Graph container below Menu container holds all the live data graphs
        self.live_data_graphs = DoubleScrolledFrame(self, relief='groove', borderwidth=2)
        self.live_data_graphs.place(relx=0.0, rely=0.05, relheight=0.95, relwidth=1)

        # Making additional containers for each graph and ease of organisation, within the Graph Container
        self.g0 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g1 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g2 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g3 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g4 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g5 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g6 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g7 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g8 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g9 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g10 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g11 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g12 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)
        self.g13 = ttk.Frame(self.live_data_graphs, relief='groove', borderwidth=2, height=200, width=400)

        # Refresh button for updating the live data graphs, placed in the Menu Container
        self.refresh_button = tk.Button(self.menu_frame, text='Refresh')
        self.refresh_button.bind("<Button>",
                                 lambda e: self.refresh_content())
        self.refresh_button.place(relx=0.5, rely=0.5, height=30, width=75, anchor=tk.CENTER)

        # Time Label, displays date and time of last refresh to user, found in Menu Container
        self.time_refreshed_label = ttk.Label(self.menu_frame)
        self.time_refreshed_label.place(x=10, y=5, height=30, width=300)
        self.update_label()

        # Historical Data Button, opens separate window for displaying historical data
        self.hist_btn = tk.Button(self.menu_frame, text='Historical Data Graph')
        self.hist_btn.bind("<Button>",
                           lambda e: HistDataPane(self, fullMarketDf=self.full_market_df))
        self.hist_btn.place(height=30, width=175, relx=0.8, rely=0.15)

    # takes slices of full_market_df based on industry and saves each slice to its own dataframe within the array
    def set_tickers(self):
        for i in range(len(self.stock_sect_arr)):
            self.stock_sect_arr[i] = self.full_market_df[self.full_market_df.Industry == self.industryList[i]].copy()

    # Method is designed to create threads (one per industry) and then calculate %age grown or fallen since last close
    def calc_percent(self):
        thread_list = []
        for i in range(len(self.industryList)):
            t = threading.Thread(target=self.calc_percent_slave, args=(i,), name=f"Thread-{i}")
            thread_list.append(t)
            t.start()
        for item in thread_list:
            item.join()

        for i in range(len(self.stock_sect_arr)):
            self.stock_sect_arr[i] = self.stock_sect_arr[i].sort_values(by='Percentage', ascending=False)

    # Slave method that each thread is targeted to when calculating %age grown or fallen
    def calc_percent_slave(self, index):
        tempPercentage = []

        for j in range(len(self.stock_sect_arr[index])):
            pre_close = self.stock_sect_arr[index].iloc[j, 3]  # Getting previous closed data using Yahoo_fin
            cmp = yf.get_live_price(
                self.stock_sect_arr[index].iloc[j, 2])  # getting current market price with Yahoo_fin

            gain_loss = cmp - pre_close
            percentage = gain_loss / pre_close * 100  # Calculating actual percentage of gain or loss
            time.sleep(0.1)  # sleep used to prevent overloading the API with requests

            tempPercentage.append(percentage)
        self.stock_sect_arr[index]['Percentage'] = tempPercentage  # Percentage of each script is
        # added as a column to each industry's data frame

    # Method is used to collect the price at which each script previously closed, thread allocated to each script
    def prev_close(self):
        threads = []
        for i in range(len(self.full_market_df)):
            t = threading.Thread(target=self.prev_close_slave, args=(i,))
            threads.append(t)
            t.start()
        # wait for all threads to finish
        for t in threads:
            t.join()

    # The slave method used by each thread of the prev_close() method
    def prev_close_slave(self, i):
        start = datetime.datetime.today() - datetime.timedelta(days=6)  # 6 day span used to allow for bank holidays,
        # and still allow data to be collected

        end = datetime.datetime.today()
        prev_close = yf.get_data(self.full_market_df.iloc[i, 2], start, end, '1d')['close'].iloc[-2]  # Collects all
        # data of a script as per parameters, then takes the second last line of data as we want previous close which
        # is the previous day

        with threading.Lock():  # Threading.lock ensures only one thread access the DF and allows for safe editing
            # that prevents data corruption
            self.full_market_df.at[i, 'Previous Close'] = prev_close

    # Method is used to create the plots for each industry's live data
    def graph_Maker(self, script, percent, mask1, mask2, min_val, max_val, title):
        fig, ax = plt.subplots(figsize=(5.75, 2), dpi=60)  # Setting each figure's size
        ax.barh(script[mask1], percent[mask1], 0.5, color='green')  # Filtering all growth scripts to green bars
        ax.barh(script[mask2], percent[mask2], 0.5, color='red')  # Filtering all falling scripts to red bars

        for s in ['top', 'bottom']:  # Setting the top and bottom edge lines to invisible
            ax.spines[s].set_visible(False)

        ax.xaxis.set_tick_params(labelsize=5)  # Setting font sizes of x and y axis ticks
        ax.yaxis.set_tick_params(labelsize=5)

        ax.grid(visible=True, color='grey',
                linestyle='-.', linewidth=0.5,
                alpha=0.2)  # Setting up grid of each plot

        ax.invert_yaxis()  # Arrange data in descending order

        # The for loop adds %age gained or loss to each bar
        for item in ax.patches:
            plt.text(item.get_width(),
                     item.get_y() + 0.25,
                     str(round((item.get_width()), 2)) + '%',
                     fontsize=6, fontweight='normal',
                     color='black')
        # Adding Plot Title
        ax.set_title(title,
                     loc='center', fontsize=6)

        ax.set_xlim(min_val, max_val)  # Setting the minimum and maximum of the x axis for scaling purposes
        return fig

    def plot_data(self):
        for i, industry in enumerate(self.stock_sect_arr): # enumerate permits use of for-each loop and provides counter

            # Creation of parameters for each industry
            script = industry.loc[:, 'Symbol']
            percent = industry.loc[:, 'Percentage']
            mask1 = percent > 0
            mask2 = percent < 0
            min_val = industry.loc[:, 'Percentage'].min() - 1
            max_val = industry.loc[:, 'Percentage'].max() + 1
            title = self.industryList[i]

            # Based on the counter value a specfic canvas is called and assigned the indutry's plot
            if i == 0:
                try:  # Try-except is used to delete a previously existing plot if there is one
                    self.c0.get_tk_widget().destroy()
                    self.c0.figure.clear()
                except:
                    pass
                # Plot is assigned to a canvas and then added to its respective container
                self.c0 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g0)
                self.c0.draw()
                self.c0.get_tk_widget().pack()
                self.g0.grid(row=0, column=0)
            elif i == 1:
                try:
                    self.c1.get_tk_widget().destroy()
                    self.c1.figure.clear()
                except:
                    pass
                self.c1 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g1)
                self.c1.draw()
                self.c1.get_tk_widget().pack()
                self.g1.grid(row=0, column=1)
            elif i == 2:
                try:
                    self.c2.get_tk_widget().destroy()
                    self.c2.figure.clear()
                except:
                    pass
                self.c2 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g2)
                self.c2.draw()
                self.c2.get_tk_widget().pack()
                self.g2.grid(row=0, column=2)
            elif i == 3:
                try:
                    self.c3.get_tk_widget().destroy()
                    self.c3.figure.clear()
                except:
                    pass
                self.c3 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g3)
                self.c3.draw()
                self.c3.get_tk_widget().pack()
                self.g3.grid(row=0, column=3)
            elif i == 4:
                try:
                    self.c4.get_tk_widget().destroy()
                    self.c4.figure.clear()
                except:
                    pass
                self.c4 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g4)
                self.c4.draw()
                self.c4.get_tk_widget().pack()
                self.g4.grid(row=1, column=0)
            elif i == 5:
                try:
                    self.c5.get_tk_widget().destroy()
                    self.c5.figure.clear()
                except:
                    pass
                self.c5 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g5)
                self.c5.draw()
                self.c5.get_tk_widget().pack()
                self.g5.grid(row=1, column=1)
            elif i == 6:
                try:
                    self.c6.get_tk_widget().destroy()
                    self.c6.figure.clear()
                except:
                    pass
                self.c6 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g6)
                self.c6.draw()
                self.c6.get_tk_widget().pack()
                self.g6.grid(row=1, column=2)
            elif i == 7:
                try:
                    self.c7.get_tk_widget().destroy()
                    self.c7.figure.clear()
                except:
                    pass
                self.c7 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g7)
                self.c7.draw()
                self.c7.get_tk_widget().pack()
                self.g7.grid(row=1, column=3)
            elif i == 8:
                try:
                    self.c8.get_tk_widget().destroy()
                    self.c8.figure.clear()
                except:
                    pass
                self.c8 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g8)
                self.c8.draw()
                self.c8.get_tk_widget().pack()
                self.g8.grid(row=2, column=0)
            elif i == 9:
                try:
                    self.c9.get_tk_widget().destroy()
                    self.c9.figure.clear()
                except:
                    pass
                self.c9 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                            master=self.g9)
                self.c9.draw()
                self.c9.get_tk_widget().pack()
                self.g9.grid(row=2, column=1)
            elif i == 10:
                try:
                    self.c10.get_tk_widget().destroy()
                    self.c10.figure.clear()
                except:
                    pass
                self.c10 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                             master=self.g10)
                self.c10.draw()
                self.c10.get_tk_widget().pack()
                self.g10.grid(row=2, column=2)
            elif i == 11:
                try:
                    self.c11.get_tk_widget().destroy()
                    self.c11.figure.clear()
                except:
                    pass
                self.c11 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                             master=self.g11)
                self.c11.draw()
                self.c11.get_tk_widget().pack()
                self.g11.grid(row=2, column=3)
            elif i == 12:
                try:
                    self.c12.get_tk_widget().destroy()
                    self.c12.figure.clear()
                except:
                    pass
                self.c12 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                             master=self.g12)
                self.c12.draw()
                self.c12.get_tk_widget().pack()
                self.g12.grid(row=3, column=1)
            elif i == 13:
                try:
                    self.c13.get_tk_widget().destroy()
                    self.c13.figure.clear()
                except:
                    pass
                self.c13 = FigureCanvasTkAgg(self.graph_Maker(script, percent, mask1, mask2, min_val, max_val, title),
                                             master=self.g13)
                self.c13.draw()
                self.c13.get_tk_widget().pack()
                self.g13.grid(row=3, column=2)


    # Method is called by the Refresh button, which updates the label and calls the previous functions to update the
    # data appropriately
    def refresh_content(self):
        self.update_label()
        self.prev_close()
        self.set_tickers()
        self.calc_percent()
        self.plot_data()

    # Method used to update the message of the label itself
    def update_label(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.time_refreshed_label.config(text=f'Data last refreshed at {current_time}, on {date.today()}')


if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
