import json
import requests

# config
from config import config, urls


class MarketService():
	tickers = []
	metadata = []


	@staticmethod
	def load_stocks(path_to_stocks):
		with open(path_to_stocks) as file:
			file_data = json.load(file)

			MarketService.tickers = file_data['tickers']
			
			# making all tickers lowercase
			for i in range(len(MarketService.tickers)):
				MarketService.tickers[i] = MarketService.tickers[i].lower()


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


	@staticmethod
	def get_tickers_data():
		params = {
			'token': config.TIINGO_API_KEY,
			'tickers': ','.join(MarketService.tickers),
		}

		data = []

		try:
			res = requests.get(urls.IEX_ENDPOINT_URL, params=params)
			data = res.json()
		except Exception as err:
			print(err)
		finally:
			return data


	@staticmethod
	def get_ticker_data(ticker):
		ticker = ticker.lower()
		
		# if passed ticker is not in the list of avaliable tickers
		if(ticker not in MarketService.tickers):
			return None
		
		params = {
			'token': config.TIINGO_API_KEY,
			'tickers': ticker,
		}

		try:
			res = requests.get(urls.IEX_ENDPOINT_URL, params=params)
			data = res.json()
			return data
		except Exception as err:
			print(err)
			return None


		
