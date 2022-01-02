from sqlite3 import connect
import pandas as pd
from sys import path
path.append('/Users/tony/Documents/programming/binance/symbols/')
from symbols import symbols

con = connect('parsed.db')
for s in symbols:
    d = pd.read_sql(f'select * from {s}', con)
    d['time'] = pd.to_datetime(d['time'] + 36000 - 0.09, unit='s')
    con2 = connect('parsed2.db')
    d.to_sql(s, con2)

con2.commit()
con.close()
con2.close()
