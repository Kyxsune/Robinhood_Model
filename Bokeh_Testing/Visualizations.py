__author__ = 'kyxsune'

from simplejson import load
from urllib import urlopen
from bokeh.models import HoverTool
from bokeh.plotting import figure,show, output_file , ColumnDataSource
from pandas import DataFrame , to_datetime
from pymongo import MongoClient


def Get_Test_Data_YQL():
    # Will have to change conver_objects to specific numeric calls in the future
    result = load(urlopen("https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22YHOO%22%20and%20startDate%20%3D%20%222010-01-11%22%20and%20endDate%20%3D%20%222010-05-10%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="))
    x = DataFrame.from_dict(result['query']['results']['quote'])
    x["Date"] = to_datetime(x["Date"])
    x = x.convert_objects(convert_numeric=True)
    return x

def Get_dataframe(Symbol):
    Symbolx = str(Symbol) + '_history'
    Db_cursor = MongoClient()['stox'][Symbolx].find()
    x = DataFrame(list(Db_cursor))
    x = x.convert_objects(convert_numeric=True)
    return x


def candle_stix(dataframe):
    '''
    This function takes in dataframes and makes a candlesticks plot using bokeh
    Parameters
    ----------
    dataframe Stock dataframe
        This frame has elements: Open, Volume, Close, High, Low, Symbol and Date
    '''
    # Develop Aspects and Calculations
    mids = (dataframe["Open"] + dataframe["Close"])/2
    spans = abs(dataframe.Close-dataframe.Open)
    inc = dataframe.Close > dataframe.Open
    dec = dataframe.Open > dataframe.Close
    w = 12*60*60*1000 #width about a half day in width

    # Define Hover tool tips
    Gain = ColumnDataSource(ColumnDataSource.from_df(dataframe[inc]))
    Loss = ColumnDataSource(ColumnDataSource.from_df(dataframe[dec]))
    hover = HoverTool(
        tooltips=[
            ("Price","$y"),
            ("High","@High"),
            ("Low","@Low"),
            ("Open","@Open"),
            ("Close","@Close"),
            ("Volume(M)","@Volume")
        ]
    )

    # Build Plot

    output_file("candlestix.html", title="Candlestix")
    TOOLS = "pan,wheel_zoom,box_zoom"
    p = figure(x_axis_type="datetime",tools=[TOOLS,hover],plot_width=800,toolbar_location="left")
    p.segment(dataframe.Time, dataframe.Low ,dataframe.Time, dataframe.High , color="black")
    p.rect(dataframe.Time[inc], mids[inc], w, spans[inc], source=Gain, fill_color="white", line_color="black")
    p.rect(dataframe.Time[dec], mids[dec], w, spans[dec], source=Loss, fill_color="black", line_color="black")
    p.title = str(str(dataframe["Symbol"][1]))
    show(p)


candle_stix(Get_dataframe("AA"))
