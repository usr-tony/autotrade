import binance
from os import environ
from symbols import symbols
from sqlite3 import connect
from time import sleep

apikey, secretkey = environ.get('api_key'), environ.get('secret_key')
bsm = binance.ThreadedWebsocketManager(api_key=apikey, api_secret=secretkey)
bsm.start()
con = {}
cur = {}
for s in symbols:
    con[s] = connect('{}.db'.format(s), check_same_thread=False)
    cur[s] = con[s].cursor()
    cur[s].execute('create table if not exists {} (time integer, price real, quantity real)'.format(s))
    

def message(msg):
    cur[msg['s']].execute(
        'INSERT INTO {} (time, price, quantity) VALUES (?,?,?)'.format(msg['s']),
        [str(msg['T']), float(msg['p']), float(msg['q'])]
    )


for s in symbols:
    bsm.start_aggtrade_socket(message, s)

while True:
    if input('type anything to close:'):
        bsm.stop()
        sleep(2)
        for s in symbols:    
            con[s].commit()
            con[s].close()