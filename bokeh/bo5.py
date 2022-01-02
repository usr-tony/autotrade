from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row, column, grid
from bokeh.models import ColumnDataSource
import binance
from symbols import symbols, colors
from functools import partial
from time import time
import numpy as np

p, ds, z = {}, {}, round(time() * 1000)

p = figure(toolbar_location=None)
p.xaxis.axis_label = 'time'
p.yaxis.axis_label = 'price'

for s in symbols:
    ds[s] = ColumnDataSource(data=dict(x=[], y=[]))
    p.line(source=ds[s], color=colors[s], line_width = 2)
    

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
    doc.add_next_tick_callback(partial(update, msg))


def update(msg):
    global z
    k = globals()[msg['s']]
    k['t'].append(msg['T'])
    k['p'].append(float(msg['p']))
    k['q'].append(msg['q'])
    t = k['t'][-1] - k['t'][0]
    dat = {
        'x' : [t],
        'y' : [k['p'][-1] / k['p'][0]]
    }
    ds[msg['s']].stream(dat, rollover=150)


def compare():
    for s in symbols:
        k = globals()[s]


soc()
