import requests, json
from config import poloniex_key, poloniex_sign
import hmac, hashlib
import urllib
import time

def api_query(command, req={}):
	req['command'] = command
	req['nonce'] = int(time.time()*1000)
	post_data = urllib.parse.urlencode(req)

	sign = hmac.new(poloniex_sign, post_data.encode('utf-8'), hashlib.sha512).hexdigest()
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Key': poloniex_key,
		'Sign': sign	
	}

	with requests.Session() as s:
		api = s.post('https://poloniex.com/tradingApi', data=post_data, headers=headers)
		data = json.loads(api.text)
	return data

def public_method(command):
	url = 'https://poloniex.com/public?command={0}'.format(command)
	api = requests.post(url, data=command)
	data = json.loads(api.text)
	return data

def bittrex_ticker():
	url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
	api = requests.get(url, params = 'none')
	data = json.loads(api.text)
	return data

def main():

	#возвращает связку USDT-BTC на  Poliniex
	last = public_method('returnTicker')
	for i in last.keys():
		if 'USDT_BTC' in i:
			print('Poloniex : ', last[i]['last'])

	#возвращает связку USDT-BTC на Bittrex
	bittrex = bittrex_ticker()	
	for i in bittrex.keys():
		if i == 'result':
			for h in bittrex[i]:
				if 'USDT-BTC' in h['MarketName']:
					print('Bittrex : ', h['Last'])

	#Возвращает баланс с Poloniex. (не забудьте добавить свой ключ и секрет в файле config.py)
	balance = api_query('returnBalances')
	for i in balance.items():
		if i[1] != '0.00000000':
			print(i[0], ': \n\t', i[1] )	 			


if __name__ == '__main__':
	main()