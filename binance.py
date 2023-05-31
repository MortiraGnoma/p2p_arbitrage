import requests
import json

base = 'https://api.binance.com'

depth = '/api/v3/depth'
info = '/api/v3/exchangeInfo'

endpoint = depth


param = {
'symbol' : 'BTCUSDT',
'limit' : '2'
}

def update(pair):
    param['symbol'] = str(pair)
    r = requests.get(base+endpoint, params = param)
    return r

def update_2(endpoint):
    r = requests.get(base+endpoint)
    return r

r = update('BTCUSDT')

#r = requests.get(base+inf)
#r = requests.get('https://www.google.com/search?q=google&oq=google&aqs=chrome..69i57j69i59j69i60l2j69i65j69i60l3.2064j0j7&sourceid=chrome&ie=UTF-8', headers = headers)

#soup = BeautifulSoup(json.dumps(r.json()['bids']), 'lxml')
def symbolList():
    r = update_2(info)
    inf = r.json()
    num = 0
    assets = []
    for s in inf['symbols']:
        assets.append(s['symbol'])
    assets = assets
    num = len(assets)
    return [assets, num]

def GetOrderbookBuy(pair):
    r = update(pair)
    return [[float(r.json()['bids'][0][0]), float(r.json()['bids'][0][1])],[float(r.json()['bids'][1][0]), float(r.json()['bids'][1][1])]]
"""
def GetOrderbookBuy(pair):
    r = update(pair)
    return [float(r.json()['bids'][0][0]), float(r.json()['bids'][0][1])]"""

def GetOrderbookSell(pair):
    r = update(pair)
    return [[float(r.json()['asks'][0][0]), float(r.json()['asks'][0][1])], [float(r.json()['asks'][1][0]), float(r.json()['asks'][1][1])]]



#print(symbolList()[0])
#print(symbolList()[1])


#val1 = json.dumps(r.json()['bids'][0][0])
#val1 = val1[1:-1]
#sum = float(val1)

#print(type(val2))
#print(val1)
#print(sum)

#i = 0
#while i < int(param['limit']):
#    print('Ціна продажу '+str(i)+': '+json.dumps(r.json()['bids'][i][0]))
#    i=i+1

#print(type(param['limit']))

#print(r.headers)
#print(r.text)
#print(soup)
