from sqlite3 import connect
import pandas as pd
from sys import path
path.append('/Users/tony/Documents/programming/binance/symbols')
from symbols import symbols

con = connect('rawdata.db')
for s in symbols:    
    d = pd.read_sql(f'select * from {s}', con)
    bid = d['bid'] != d['bid'].shift(1)  
    ask = d['ask'] != d['ask'].shift(1)
    bidask = bid | ask
    d = d[bidask]
    print(d)
    con2 = connect('parsed.db')
    d.to_sql(s, con2)
    con2.commit()

con.close()
con2.close()
