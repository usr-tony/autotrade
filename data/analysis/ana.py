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


def main():
    wheelzoom = WheelZoomTool()
    fig = figure(x_axis_type='datetime', tools=[ResetTool(), PanTool(), wheelzoom, HoverTool()], active_scroll=wheelzoom)
    fig.xaxis.axis_label='time'
    fig.yaxis.axis_label='price'
    i_time = 1630680353.514287
    ct = 300
    dt = 30
    i = 0
    for s in symbols:
        con = connect('book.db')
        d = read_sql(
            f'select * from {s} where time > {i_time} and time < {i_time} + {ct}',
            con
        )
        d = d.drop(columns='index')
        datadic = {
            'time' : [],
            'bid' : [],
            'ask' : []
        }
        for i in range(1, len(d['time'])):
            bid = d.iloc[i]['bid']
            mean_df = d.loc[(d['time'] < d.iloc[i]['time']) & (d['time'] > d.iloc[i]['time'] - dt)]['bid']
            if mean_df.empty:
                d.drop(index=i)
                print('no mean at', s, 'index: ', i)
            else:
                meanbid = mean_df.mean()
                datadic['bid'].append(bid/meanbid*100)

        d['time'] = to_datetime(d['time'] + 36000, unit='s')
        mean_bid = d['bid'].mean()
        d['bid'] = d['bid']/mean_bid * 100
        d['ask'] = d['ask']/mean_bid * 100
        fig.segment(x0=d['time'], y0=datadic['bid'], x1=d['time'], y1=d['ask'], color=colors[s])

    doc = curdoc()
    doc.add_root(row(fig, sizing_mode='stretch_both'))
    show(fig)


if __name__=='__main__':
    main()

