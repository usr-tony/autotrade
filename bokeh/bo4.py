import multiprocessing
from bokeh.plotting import curdoc, figure
from bokeh.layouts import layout, row, column, grid
from bokeh.models import ColumnDataSource
import binance
from symbols import symbols
from functools import partial
import numpy as np

p, ds, z = {}, {}, 0

for s in symbols:
    ds[s] = ColumnDataSource(data=dict(x=[], y=[]))
    p[s] = figure(title=s, toolbar_location=None)
    p[s].xaxis.axis_label = 'time'
    p[s].yaxis.axis_label = 'price'
    l = p[s].line(source=ds[s])
    

doc = curdoc()
doc.add_root(row([p[s] for s in p], sizing_mode='stretch_both'))


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
    #changes timestamp to something readable
    doc.add_next_tick_callback(partial(update, msg))


def update(msg):
    global z
    if z==0:
        z = msg['T']
    s = msg['s']
    t = msg['T'] - z
    print(msg['a'])
    dat = {
        'x' : [t],
        'y' : [msg['p']]
    }
    ds[s].stream(dat, rollover=100)


soc()
