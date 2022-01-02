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


def init():
    global ds
    p, ds, z = {}, {}, round(time() * 1000)

    p = figure(toolbar_location=None)
    p.xaxis.axis_label = 'time'
    p.yaxis.axis_label = 'price'

    for s in symbols:
        ds[s] = ColumnDataSource(data=dict(x=[], y=[]))
        p.line(source=ds[s], color=colors[s], line_width = 2)
        
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
    k['t'].append(msg['T'])
    k['p'].append(float(msg['p']))
    k['q'].append(msg['q'])
    t = k['t'][-1] - dt[s]
    dat = {
        'x' : [t],
        'y' : [k['p'][-1] / meanp[s]]
    }
    ds[s].stream(dat, rollover=150)


def ref():
    global meanp, meanq, tabls, dt
    meanp, cum_q, tabls, dt, = {}, {}, {}, {}
    sleep(1)
    while True:
        for s in symbols:
            k = globals()[s]
            t = k['t']
            dt[s] = t[-1] - 30000
            for i in range(len(t)):
                if t[-i] - dt <= 0:
                    dt = t[-i]
                    break
                dt[s] = t[0]
            
            for l in k:
                k[l] = k[l][-i:]
            
            ks = pd.DataFrame(k)
            meanp[s] = ks.mean('p')
            print(ks.mean['p'])
            cum_q[s] = ks.cumsum('q')
            sleep(5)


init()
t1 = Thread(target=soc())
t2 = Thread(target=ref)
t1.start()
