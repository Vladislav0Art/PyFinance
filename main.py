import telebot

# config
from config import config
from config import db

# services
from services.bot.BotService import BotService
from services.market.MarketService import MarketService
from services.competition.CompetitionService import CompetitionService



with db.Session() as session:
	bot  = telebot.TeleBot(token=config.TELEGRAM_BOT_API_KEY)

	# setting metadata for avaliable tickers
	MarketService.load_stocks('config/stocks.json')
	MarketService.set_tickers_metadata()

	# initializing bot service
	botService = BotService(session, bot)


	# initializing competition service
	CompetitionService.start({
		'session': session,
		'bot': bot,
		'duration': 60 * 60 * 24 * 7  # 7 days
	})

	# /start - sends bot info
	@bot.message_handler(commands=['start'])
	def send_bot_info(message):
		response = '<strong>Welcome to PyFinance bot - a trading competition platform created as a Python project by @Vladislav0Art</strong>\n\n<b>The rules are as follows:</b>\n1) Each week at Sunday {default_usd}$ is assigned to your account.\n2) You have exactly one week of trading, next Sunday is the deadline\n3) After deadline top 10 players will be Competition Winners\n4) Then it starts over again, as simple as that\n\nIf you want to know about supported commands type /help\n\n<b>P.S.1</b> The codebase for this project is complete mess, please do not judge the author, he has spent on this project too little amount of time to make it decent :(\n\n<b>P.S.2</b> Warning: bugs and undesired effects may occur. Even author has no idea that might happen...'.format(default_usd=config.COMPETITION_DEFAULT_USD_AMOUNT)

		bot.send_message(message.chat.id, response, parse_mode='HTML')

	

	# /help - sends a list with avaliable commands
	@bot.message_handler(commands=['help'])
	def send_help_info(message):
		response = "\
			1\) /start \- show basic information about the project\n\n\
			2\) /register \- registers new user \(required to have access to most of the commands, **first command you need to type**\)\n\n\
			3\) /participate \- sets a user as a participant \(required to have access to trading\)\n\n\
			4\) /market [ticker] \- shows a list of avaliable stocks on the PyFinance trading platform\. If ticker is specified shows detailed info about the ticker; ticker can be typed in either lower or upper case\. Example: `/market AAPL`\n\n\
			5\) /assets \- shows all user assets and transactions made during current competition\n\n\
			6\) /ranking [competition id] \- if [competition id] is not provided shows results of the current competition, otherwise shows results of the competition with the provided id\. Example: `/ranking 0`\n\n\
			7\) /buy [stock ticker] [amount] \- buys a stock at specified amount\. Ticker can be typed in either lower and upper cases\. Example: `/buy AAPL 3`\n\n\
			8\) /sell [stock ticker] [amount] \- sells a stock at specified amount\. Ticker can be typed in either lower and upper cases\. Example: `/sell AAPL 3`\n\
		"

		bot.send_message(message.chat.id, response, parse_mode='MarkdownV2')



	# /participate - enrolls user into competition
	@bot.message_handler(commands=['participate'])
	def start_competition_handler(message):
		botService.enroll_user_in_competition(message)


	# /register - creates user instance in db
	@bot.message_handler(commands=['register'])
	def user_registration_handler(message):
		botService.register_user(message)

	# /market [ticker] - returns market data for avaliable tickers
	@bot.message_handler(commands=['market'])
	def send_market_data_handler(message):
		botService.send_market_data(message)


	# /buy [ticker] [amount] - buying a ticker of specific amount 
	@bot.message_handler(commands=['buy'])
	def buy_ticker_handler(message):
			botService.buy_ticker(message)


	# /sell [ticker] [amount] - selling a ticker of specific amount
	@bot.message_handler(commands=['sell'])
	def sell_ticker_handler(message):
		botService.sell_ticker(message)


	# /ranking [competition_id] - prints ranking of the competition with passed id or the current competition
	@bot.message_handler(commands=['ranking'])
	def send_ranking_data_handler(message):
		botService.send_ranking_data(message)


	# /assets [ticker] - prints assets info
	@bot.message_handler(commands=['assets'])
	def send_assets_data_handler(message):
		botService.send_assets_data(message)

	# running
	telebot.apihelper.SESSION_TIME_TO_LIVE = 20 * 60
	bot.infinity_polling()