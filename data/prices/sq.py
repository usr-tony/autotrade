from sqlite3 import connect
from datetime import datetime

con = connect('DOGEUSDT.db')
cur = con.cursor()
count = 0
for row in cur.execute('select * from DOGEUSDT'):
    print(row)
    count+=1
print('number of rows: ', count)

con.close()