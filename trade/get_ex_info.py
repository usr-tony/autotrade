from binance import AsyncClient
from os import environ
from time import *
from asyncio import run


async def main():
    client = await AsyncClient.create(api_key=environ.get('apikey'), api_secret=environ.get('secretkey'))
    res = await get_exchange_info(client)
    print(res)


async def get_exchange_info(client):
    ex_info = {}
    r = await client.futures_exchange_info()
    for row in r['symbols']:
        k = row['filters']
        d = ex_info[row['symbol']] = {}
        d['minQty'] = k[1]['minQty']
        d['tickSize'] = k[0]['tickSize']
    
    return ex_info
         

if __name__ == '__main__':
    data = run(main())