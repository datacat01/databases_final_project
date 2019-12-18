import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import datetime
from decimal import Decimal
import pandas as pd


matplotlib.use('Agg')


class GenerateGraphs:
    def __init__(self, usr_id):
        self.__usr_id = usr_id
    
    def get_sales_data(self):
        print(self.__sales_data)
    
    def get_orders_data(self):
        print(self.__orders_data)
    
    def set_sales_data(self, new_sales_data):
        self.__sales_data = pd.DataFrame(list(new_sales_data), columns=[1,2,'date','profit'], dtype=float)
        self.__sales_data = self.__sales_data[['date','profit']].copy()
    
    def set_orders_data(self, new_orders_data):
        self.__orders_data = pd.DataFrame(list(new_orders_data), columns=[1,2,3,'ord_time','paym_time'], dtype=float)
        self.__orders_data = self.__orders_data[['ord_time','paym_time']].copy()
    
    def sales_lineplot(self):
        self.__sales_data.date = self.__sales_data['date'].map(lambda x:x.date())
        df_groupedby_date = self.__sales_data.groupby('date').sum()
        df_groupedby_date.reset_index(inplace=True)

        fig = plt.figure(figsize=(15, 8), dpi=200)
        plt.plot_date(x=df_groupedby_date.date, y=df_groupedby_date.profit, ls='-', lw=2, c='indianred')
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.xticks(rotation=35)

        name = f'static/images/charts/sales_statistics_overview_{self.__usr_id}.png'
        plt.savefig(name)

        return datetime.datetime.now()
    
    def orders_per_day(self):
        self.__orders_data.ord_time = self.__orders_data['ord_time'].map(lambda x:x.date())
        df_groupedby_date = self.__orders_data.groupby('ord_time').count()
        df_groupedby_date.reset_index(inplace=True)

        fig = plt.figure(figsize=(5, 4), dpi=200)
        plt.plot_date(x=df_groupedby_date.ord_time, y=df_groupedby_date.paym_time, ls='-', lw=2, c='blue')
        plt.xlabel('Date')
        plt.ylabel('Orders count')
        plt.xticks(rotation=35)

        name = f'static/images/charts/ordrs_per_day_{self.__usr_id}.png'
        plt.savefig(name)

        return datetime.datetime.now()
    
    def av_time(self):
        self.__orders_data['duration'] = self.__orders_data.paym_time - self.__orders_data.ord_time
        
        fig = plt.figure(figsize=(5, 4), dpi=200)
        plt.plot_date(x=self.__orders_data.ord_time, y=self.__orders_data.duration, ls='-', lw=2, c='midnightblue')
        plt.xlabel('Date')
        plt.ylabel('Time spent')
        plt.xticks(rotation=35)

        name = f'static/images/charts/av_time_{self.__usr_id}.png'
        plt.savefig(name)

        return datetime.datetime.now()


if __name__ == "__main__":
    s = GenerateGraphs(1)
    s.set_orders_data(((19, None, Decimal('569.00'), datetime.datetime(2019, 12, 19, 17, 20), datetime.datetime(2019, 12, 19, 18, 50)), (2, 3, Decimal('45.00'), datetime.datetime(2019, 12, 19, 12, 12), datetime.datetime(2019, 12, 19, 15, 34)), (3, 3, Decimal('45.00'), datetime.datetime(2019, 12, 19, 12, 12), datetime.datetime(2019, 12, 19, 15, 34)), (18, None, Decimal('98.90'), datetime.datetime(2019, 12, 17, 10, 12), datetime.datetime(2019, 12, 17, 11, 58)), (20, 11, Decimal('56.00'), datetime.datetime(2019, 12, 13, 9, 4), datetime.datetime(2019, 12, 13, 10, 16)), (9, None, Decimal('344.00'), datetime.datetime(2019, 12, 8, 9, 45), datetime.datetime(2019, 12, 8, 11, 22)), (1, 1, Decimal('117.00'), datetime.datetime(2019, 12, 5, 16, 14), datetime.datetime(2019, 12, 5, 18, 19)), (6, 1, Decimal('67.40'), datetime.datetime(2019, 12, 5, 13, 43), datetime.datetime(2019, 12, 5, 17, 19)), (8, None, Decimal('343.00'), datetime.datetime(2019, 12, 5, 12, 40), datetime.datetime(2019, 12, 5, 17, 43)), (7, None, Decimal('598.00'), datetime.datetime(2019, 12, 3, 16, 8), datetime.datetime(2019, 12, 3, 14, 15)), (17, 11, Decimal('166.00'), datetime.datetime(2019, 9, 9, 9, 13), datetime.datetime(2019, 9, 9, 10, 41))))
    s.av_time()

