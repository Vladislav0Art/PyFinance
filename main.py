import telebot

# config
from config import config
from config import db

# services
from services.bot.BotService import BotService
from services.market.marketService import MarketService



with db.Session() as session:
	bot  = telebot.TeleBot(token=config.TELEGRAM_BOT_API_KEY)

	# initializing bot service
	botService = BotService(session, bot)

	# setting metadata for avaliable tickers
	MarketService.load_stocks('config/stocks.json')
	MarketService.set_tickers_metadata()


	# /start - enrolls user into competition
	@bot.message_handler(commands=['start', 'participate'])
	def handler_start_competition(message):
		botService.enroll_user_in_competition(message)


	# /register - creates user instance in db
	@bot.message_handler(commands=['register'])
	def handler_user_registration(message):
		botService.register_user(message)


	# running
	bot.infinity_polling()