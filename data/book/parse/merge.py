import sys
sys.path.append('/Users/tony/Documents/programming/binance/symbols')
from symbols import symbols
from sqlite3 import connect
import pandas as pd

for s in symbols:
    con = connect('rawdata.db')
    cur = con.cursor()
    cur.execute(f"attach database '{s}.db' as old_db")
    cur.execute(f'create table {s} (time real, bid real, ask real, bidq real, askq real)')
    cur.execute(f'insert into {s} select * from old_db.{s}')
    con.commit()
    con.close()

    
