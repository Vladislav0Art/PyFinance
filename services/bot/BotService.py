# methods
from services.bot.methods.enroll_user_in_competition import enroll_user_in_competition
from services.bot.methods.register_user import register_user
from services.bot.methods.send_market_data import send_market_data
from services.bot.methods.buy_ticker import buy_ticker


class BotService():
	def __init__(self, session, bot):
		self.session = session
		self.bot = bot

	def enroll_user_in_competition(self, message):
		enroll_user_in_competition(self.session, self.bot, message)

	def register_user(self, message):
		register_user(self.session, self.bot, message)

	def send_market_data(self, message):
		send_market_data(self.bot, message)

	def buy_ticker(self, message):
		buy_ticker(self.session, self.bot, message)