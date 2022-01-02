from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row, column, grid
from bokeh.models import ColumnDataSource
import binance
from symbols import symbols, colors
from functools import partial
from time import time, sleep
import numpy as np
import pandas as pd
from threading import Thread
#relative prices from last 2s mean price
meanp, cumq, tabls, dt, ds = {}, {}, {}, {}, {}

def init():
    global ds
    p = figure(toolbar_location=None, y_range=(0.99, 1.01))
    p.xaxis.axis_label = 'time'
    p.yaxis.axis_label = 'price'
    for s in symbols:
        ds[s] = ColumnDataSource(data=dict(x=[], y=[]))
        p.line(source=ds[s], color=colors[s], line_width = 2, legend_label=s)
        
    global doc
    doc = curdoc()
    doc.add_root(row(p, sizing_mode='stretch_both'))


def soc():
    bsm = binance.ThreadedWebsocketManager()
    bsm.start()
    for s in symbols:
        globals()[s] = {
            't' : [],
            'p' : [],
            'q' : []
        }
        bsm.start_aggtrade_socket(message, s)


def message(msg):
    updated = partial(update, msg, msg['s'])
    doc.add_next_tick_callback(updated)


def update(msg, s):
    k = globals()[s]
    k['t'].append(int(msg['T']))
    k['p'].append(float(msg['p']))
    k['q'].append(float(msg['q']))
    t = k['t'][-1]
    try:
        dat = {
            'x' : [t],
            'y' : [k['p'][-1] / meanp[s]]
        }
    except:
        dat = {
            'x' : [t],
            'y' : [k['p'][-1]/k['p'][0]]
        }
    
    ds[s].stream(dat, rollover=75)


def ref():
    global meanp, cumq, tabls, dt
    for s in symbols:
        k = globals()[s]
        t = k['t']
        dt[s] = t[-1] - 2000
        for i in range(1, len(t)):
            if t[-i] - dt[s] <= 0:
                dt[s] = t[-i]
                break
            dt[s] = t[0]

        for l in k:
            k[l] = k[l][-i:]
        
        ks = pd.DataFrame(k)
        meanp[s] = ks['p'].mean()
        cumq[s] = ks['q'].cumsum().iloc[-1]

def loop():
    while True:
        sleep(2)
        try:
            ref()
        except:
            pass


if 'bokeh_app' in __name__:
    init()
    t1 = Thread(target=soc)
    t2 = Thread(target=loop)
    t1.start()
    t2.start()