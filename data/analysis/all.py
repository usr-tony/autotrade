import pandas as pd
from sys import path
from pandas.core.tools.datetimes import to_datetime

from pandas.io.sql import read_sql
from symbols import symbols, colors
from sqlite3 import connect
import datetime as dt
from bokeh.plotting import figure, show, curdoc
from bokeh.models import ColumnDataSource, WheelZoomTool, BoxZoomTool, HoverTool, PanTool, ResetTool
from bokeh.layouts import row
from pandas import DataFrame
from pandas import NA


def run(ct = 60, i_time = 1630680353 + 36000):
    i_time = int(i_time) - 36000
    ct = int(ct)
    dt = 30
    wheelzoom = WheelZoomTool()
    hovertool = HoverTool(
        tooltips=[
            ('datetime', '@x0{0}'),
            ('ask', '@y1'),
            ('bid', '@y0'),
            ('name', '$name')
        ]
    )
    fig = figure(x_axis_type='datetime', tools=[ResetTool(), PanTool(), wheelzoom, hovertool], active_scroll=wheelzoom)
    fig.xaxis.axis_label='time'
    fig.yaxis.axis_label='price'
    i = 0
    meanlist = []
    for s in symbols:
        con = connect('book.db')
        d = read_sql(
            f'select * from {s}',
            con
        )
        d = d.drop(columns='index')

        d['time'] = to_datetime(d['time'] + 36000, unit='s')
        initial_bid = d['bid'][0]
        d['bid'] = d['bid']/initial_bid * 100
        d['ask'] = d['ask']/initial_bid * 100
        fig.segment(x0=d['time'], y0=d['bid'], x1=d['time'], y1=d['ask'], color=colors[s], name=s)
        
        

    doc = curdoc()
    doc.add_root(row(fig, sizing_mode='stretch_both'))
    show(fig)


if __name__=='__main__':
    run()

