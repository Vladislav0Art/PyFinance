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
		'duration': 30 # 60 * 60 * 24 * 7  # 7 days
	})



	# /start - enrolls user into competition
	@bot.message_handler(commands=['start', 'participate'])
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

	# running
	telebot.apihelper.SESSION_TIME_TO_LIVE = 20 * 60
	bot.infinity_polling()