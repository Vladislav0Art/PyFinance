# methods
from services.bot.methods.enroll_user_in_competition import enroll_user_in_competition
from services.bot.methods.register_user import register_user
from services.bot.methods.send_market_data import send_market_data
from services.bot.methods.buy_ticker import buy_ticker
from services.bot.methods.access_validation import check_registration, check_participating


class BotService():
	def __init__(self, session, bot):
		self.session = session
		self.bot = bot


	# @ACCESS: public
	def enroll_user_in_competition(self, message):
		enroll_user_in_competition(self.session, self.bot, message)


	# @ACCESS: public
	def register_user(self, message):
		register_user(self.session, self.bot, message)


	# @ACCESS: public
	def send_market_data(self, message):
		send_market_data(self.bot, message)


	# @ACCESS: private
	def buy_ticker(self, message):
		user_id = message.from_user.id

		# if user is registered and participates in competition
		if (check_registration(self.session, user_id) and check_participating(self.session, user_id)):
			buy_ticker(self.session, self.bot, message)
		else:
			self.bot.send_message(message.chat.id, 'To access the API you have to start participating in the current competition and to be registered')