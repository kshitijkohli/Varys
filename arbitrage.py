import requests, json, csv


def main():
	# Binance
	url = 'https://api3.binance.com/api/v3/ticker/price'
	response = requests.get(url)
	binanceData = json.loads(response.content.decode('utf-8'))
	# print(json.dumps(body,indent=4))




	# Wazir
	url = 'https://api.wazirx.com/api/v2/tickers'
	response = requests.get(url)
	wazirData = json.loads(response.content.decode('utf-8'))
	# print(json.dumps(body,indent=4))

	wazirData =  {k.upper(): v for k, v in wazirData.items()}

	symbolList = []

	for coin in binanceData:
		symbolList.append([coin["symbol"],coin["price"]])

	# for coin in symbolList:
		# print(coin[1])

	arbitrageList = []

	exceptionList = ["BCHSVUSDT"]

	for key in symbolList:
		coin = {}
		symbol = key[0]
		print(symbol)
		if symbol in wazirData.keys() and symbol not in exceptionList:
			wazirPrice = float(wazirData[symbol]["last"])
			# print(wazirPrice)
			binancePrice = float(key[1])
			# print("printing prices")
			# print(type(binancePrice))
			# print(type(wazirPrice))
			variation = abs(((binancePrice-wazirPrice)/(binancePrice))*100)
			variation = round(variation,2)
			coin.update({
				"symbol" : symbol,
				"wazirPrice" : wazirPrice,
				"binancePrice" : binancePrice,
				"variation" : variation
				})
			if int(wazirPrice) != 0:
				arbitrageList.append(coin)


	for coin in arbitrageList:
		print(coin)

	output = []
	output.append(["Symbol","Wazir Price","Binance Price","Variation"])
	for coin in arbitrageList:
		output.append([coin["symbol"],coin["wazirPrice"],coin["binancePrice"],coin["variation"]])
	with open('arbitrage.csv', 'a+') as f:
	    write = csv.writer(f)
	    write.writerows(output)



if __name__ == '__main__':
	main()