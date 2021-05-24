import requests, json, csv, operator
from collections import namedtuple
from itertools import islice
import csv

PRICE_EPSILON = 0.00000001

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def getData(url):
        response = requests.get(url)
        return json.loads(response.content.decode('utf-8'))


#Data: { symbol: [ highest buy order active, lowest sell order active]
def getBinanceData():
        URL = 'https://api3.binance.com/api/v3/ticker/price'
        data = getData(URL)
        data = { v["symbol"].upper(): [float(v["price"]), float(v["price"])] for v in data}   
##        print(take(2, aa.items()))
        return data

def getWazirData():
        URL = 'https://api.wazirx.com/api/v2/tickers'
        data = getData(URL)
        data = {k.upper(): [float(v["buy"]), float(v["sell"])] for k,v in data.items()}
        return data
        #print(data)
##        for k,v in data.items():
##            if v[0] < PRICE_EPSILON:
##                print(k)

def getZebpayData():
        URL = 'https://www.zebapi.com/pro/v1/market/'
        data = getData(URL)
        data = list(filter(lambda i: "buy" in i and "sell" in i and "pair" in i, data))
        data = { v["pair"].upper().replace("-", ""): [float(v["sell"]), float(v['buy'])] for v in data}   
##        print(take(2, data.items()))
        return data

def calcDiff(exchangeData1, exchangeData2, name1, name2):
        diff = []
        for k,v1 in exchangeData1.items():
                v2 = exchangeData2.get(k)
                if v2 is None:
                        continue

                if v1[0] < PRICE_EPSILON or v1[1] < PRICE_EPSILON or v2[0] < PRICE_EPSILON or v2[1] < PRICE_EPSILON:
                        continue
                
                variation = ((v1[0]-v2[1])/(v2[1]))*100
                variation = round(variation,2)
                trade = {
                        "symbol" : k,
                        name1 : v1[0],
                        name2 : v2[1],
                        "variation" : variation
                        }
                diff.append(trade)
                
                variation = ((v2[0]-v1[1])/(v1[1]))*100
                variation = round(variation,2)
                trade = {
                        "symbol" : k,
                        name1 : v1[1],
                        name2 : v2[0],
                        "variation" : variation
                        }
                diff.append(trade)
        
        diff.sort(key = lambda i: i['variation'], reverse = True)
        return diff


zeroFeeListWB = {"usdt","btc","bnb","wrx","zil","eth","ada","link","waves","band","dgb","doge","eos","atom","zec","algo","uni","xtz","hbar","enj","vet",
                 "dot","xem","yfi","ren","egld","grs","comp","kava","aave","cos","inj","snx","sushi","dock","avax","iotx","aion","bal","bnt","uma","ksm",
                 "luna","grt","paxg","zrx","ankr","xym","ckb","vib","paxg","gto","tko","crv","mana","dexe","etc","ftm","fet","fil","win","sc","cvc",
                 "cake","iost","ftt","avax","luna","ava","xvg","shib","kmd"}


def filterZeroFeeWB(diff):
        filtered = []
        for trade in diff:
                symbol = trade["symbol"]
                if symbol.endswith("USDT"):
                        if symbol[:-4].lower() in zeroFeeListWB:
                                filtered.append(trade)
        return filtered

def calcArbitrage(code):
        
        if code == 0:
                diff = calcDiff(getBinanceData(), getWazirData(), "binance", "wazir")
                diff = filterZeroFeeWB(diff)
                return diff
        elif code == 1:
                diff = calcDiff(getZebpayData(), getWazirData(), "zebpay", "wazir")
                return diff
                
        print ("invalid input code")


def main():
        diff = calcArbitrage(1)
        

        exceptionList = {"BCHSVUSDT"}	
        arbitrageList = list(filter(lambda i: i["symbol"] not in exceptionList, diff)) 
	
        for coin in arbitrageList[:20]:
                print(coin)

##        keys = arbitrageList[0].keys()
##        with open('arbitrage.csv', 'w', newline='')  as output_file:
##                dict_writer = csv.DictWriter(output_file, keys)
##                dict_writer.writeheader()
##                dict_writer.writerows(arbitrageList)


if __name__ == '__main__':
	main()
