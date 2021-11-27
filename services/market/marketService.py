import json
from os import stat
import requests

# config
from config import config, urls


class MarketService():
	tickers = []
	metadata = []


	# loading json file with tickers
	@staticmethod
	def load_stocks(path_to_stocks):
		with open(path_to_stocks) as file:
			file_data = json.load(file)

			MarketService.tickers = file_data['tickers']
			
			# making all tickers lowercase
			for i in range(len(MarketService.tickers)):
				MarketService.tickers[i] = MarketService.tickers[i].lower()



	# sets name and ticker of stocks to metadata prop of class
	@staticmethod
	def set_tickers_metadata():
		params = {
			'token': config.TIINGO_API_KEY,
			'tickers': ','.join(MarketService.tickers),
		}
		
		result = []

		try:
			res = requests.get(urls.METADATA_ENDPOINT_URL, params=params)
			data = res.json()

			for ticker_data in data:
				# if ticker is not active on market
				if(not ticker_data['isActive']): 
					continue

				ticker_meta = {
					'ticker': ticker_data['ticker'],
					'name': ticker_data['name']
				}
				result.append(ticker_meta)

		except Exception as err:
			print(err)

		finally:
			MarketService.metadata = result



	# retrieves specified props of api response object and sets them to ticker data
	@staticmethod
	def retrieve_tickers(data) -> list:
		result = []

		for ticker in data:
			ticker_data = {
				'ticker': ticker['ticker'],
				'bidPrice': ticker['bidPrice'], 
				'askPrice': ticker['askPrice'],
				'bidSize': ticker['bidSize'],
				'askSize': ticker['askSize'],
				'last': ticker['last'],
				'low': ticker['low'],
				'high': ticker['high'],
				'open': ticker['open'],
				'prevClose': ticker['prevClose'],
				'isAbleToBuy':	(ticker['askSize'] is not None) and \
								(ticker['askSize'] > 0) and \
								(ticker['askPrice'] is not None) and \
								(ticker['askPrice'] > 0),
				'isAbleToSell':	(ticker['bidSize'] is not None) and \
								(ticker['bidSize'] > 0) and \
								(ticker['bidPrice'] is not None) and \
								(ticker['bidPrice'] > 0),
			}
			
			# searching for ticker name
			for current_ticker_info in MarketService.metadata:
				if(current_ticker_info['ticker'] == ticker['ticker'].lower()):
					ticker_data['name'] = current_ticker_info['name']
					break
			
			result.append(ticker_data)
		
		return result



	# returns data of all application tickers from the api 
	@staticmethod
	def get_market_data() -> list:
		result = []

		params = {
			'token': config.TIINGO_API_KEY,
			'tickers': ','.join(MarketService.tickers),
		}

		try:
			res = requests.get(urls.IEX_ENDPOINT_URL, params=params)
			result = MarketService.retrieve_tickers(res.json())
		
		except Exception as err:
			print(err)

		finally:
			return result



	# returns list of data of all tickers passed in a list
	@staticmethod
	def get_tickers_data(tickers) -> list:
		filtered_tickers = []
		result = []

		# filtering passed tickers and lowercasing them
		for ticker in tickers:
			lowercased_ticker = ticker.lower()

			if(lowercased_ticker in MarketService.tickers):
				filtered_tickers.append(lowercased_ticker)
		

		params = {
			'token': config.TIINGO_API_KEY,
			'tickers': ','.join(filtered_tickers),
		}

		try:
			res = requests.get(urls.IEX_ENDPOINT_URL, params=params)
			result = MarketService.retrieve_tickers(res.json())
			
		except Exception as err:
			print(err)
		
		finally:
			return result


	@staticmethod
	def get_ticker_ask_price(ticker):
		ticker_data = MarketService.get_tickers_data([ticker])
		ask_price = None
		
		if(len(ticker_data) > 0 and ticker_data[0]['isAbleToBuy']):
			ask_price = ticker_data[0]['askPrice']

		return ask_price


	
	@staticmethod
	def get_ticker_bid_price(ticker):
		ticker_data = MarketService.get_tickers_data([ticker])
		bid_price = None

		if(len(ticker_data) > 0 and ticker_data[0]['isAbleToSell']):
			bid_price = ticker_data[0]['bidPrice']

		return bid_price

	
	@staticmethod
	def get_ticker_name(ticker):
		ticker = ticker.lower()
		name = None

		for ticker_metadata in MarketService.metadata:
			if ticker_metadata['ticker'] == ticker:
				name = ticker_metadata['name']
				break
			
		return name


	@staticmethod
	def does_ticker_exist(ticker):
		return ticker.lower() in MarketService.tickers