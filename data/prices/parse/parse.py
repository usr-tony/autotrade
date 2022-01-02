from sqlite3 import connect
from sys import path
import datetime
from pandas import read_sql
path.append('/Users/tony/Documents/programming/binance/symbols')
from symbols import symbols
import pandas as pd

con1 = connect('prices.db')
for s in symbols:    
    con2 = connect(f'{s}.db')
    d = read_sql(f'select * from {s}', con2)
    d['time'] = d['time']/1000
    d.to_sql(s, con1)
