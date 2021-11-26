from services.market.MarketService import MarketService


# returns list of provived tickers after main command
def get_provided_tickers(command):
	# retrieving params passed after main command
	tickers = command.split(' ')[1::]
	return tickers


# iterates through tickers and apply passed template
def format_data_via_template(data, template):
	response_text = ''

	# formatting data from ticker
	for ticker in data:
		for key in ticker:
			if ticker[key] is None:
				ticker[key] = '-'

		ticker_text = template.format(ticker=ticker)
		response_text += ticker_text
	
	return response_text


# returns ticker template according to passed tempate type
def get_ticker_template(template_type):
	minimal_ticker_template = "\
		<b>Ticker: </b> {ticker[ticker]}\n\
		<b>Name: </b> {ticker[name]}\n\
		<b>Price: </b> {ticker[askPrice]}\
	\n\n"

	detailed_ticker_template = "\
		<b>Ticker: </b> {ticker[ticker]}\n\
		<b>Name: </b> {ticker[name]}\n\
		<b>Bid price: </b> {ticker[bidPrice]}\n\
		<b>Bid size: </b> {ticker[bidSize]}\n\
		<b>Ask price: </b> {ticker[askPrice]}\n\
		<b>Ask size: </b> {ticker[askSize]}\n\
		<b>Last trade: </b> {ticker[last]}\n\
		<b>Low price: </b> {ticker[low]}\n\
		<b>High price: </b> {ticker[high]}\n\
		<b>Open price: </b> {ticker[open]}\n\
		<b>Previous close price: </b> {ticker[prevClose]}\
	\n\n"

	template = None

	if template_type == 'minimal': 
		template = minimal_ticker_template
	elif template_type == 'detailed':
		template = detailed_ticker_template

	return template


# sends data of market tickers or data of provided tickers
def send_market_data(bot, message):
	provided_tickers = get_provided_tickers(message.text)

	# if ticker was provided
	if(len(provided_tickers) > 0):
		data = MarketService.get_tickers_data(provided_tickers)		
		response_template = get_ticker_template('detailed')

		# if provided tickers are incorrect
		if(len(data) <= 0):
			return bot.send_message(message.chat.id, 'You have provided non-existing tickers')

	else:
		data = MarketService.get_market_data()
		response_template = get_ticker_template('minimal')
		
		# if stock market has no tickers
		if len(data) <= 0:
			return bot.send_message(message.chat.id, 'There are no avaliable stocks on PyFinance Market right now')


	response_text = '<strong>PyFinance Stock Market:</strong>\n\n'
	response_text += format_data_via_template(data, response_template)
	response_text += '\nAll prices are specified in USD\n\n'

	bot.send_message(message.chat.id, text=response_text, parse_mode='HTML')


