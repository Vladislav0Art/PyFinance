import json
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

		# filtering passed tickers
		for ticker in tickers:
			lowered_ticker = ticker.lower()

			if(lowered_ticker in MarketService.tickers):
				filtered_tickers.append(lowered_ticker)
		

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
