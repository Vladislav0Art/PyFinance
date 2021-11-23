import telebot

# order matters: models come first, then comes db module
from config import config
from config import db

# bot api handlers
from api.bot.enroll_user_in_competition import enroll_user_in_competition
from api.bot.register_user import register_user





with db.Session() as session:
	bot  = telebot.TeleBot(token=config.TELEGRAM_BOT_API_KEY)

	# /start - enrolls user into competition
	@bot.message_handler(commands=['start', 'participate'])
	def handler(message):
		enroll_user_in_competition(session, bot, message)


	# /register - creates user instance in db
	@bot.message_handler(commands=['register'])
	def handler(message):
		register_user(session, bot, message)



	# running
	bot.polling(none_stop=True)