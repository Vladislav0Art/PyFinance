# methods
from services.bot.methods.enroll_user_in_competition import enroll_user_in_competition
from services.bot.methods.register_user import register_user
from services.bot.methods.send_market_data import send_market_data
from services.bot.methods.buy_ticker import buy_ticker
from services.bot.methods.access_validation import check_registration, check_participating
from services.bot.methods.sell_ticker import sell_ticker
from services.bot.methods.send_ranking_data import send_ranking_data
from services.bot.methods.send_assets_data import send_assets_data


class BotService():
	def __init__(self, session, bot):
		self.session = session
		self.bot = bot

	# if user is registered and participates in competition call passed callback
	def with_access(self, message, callback):
		user_id = message.from_user.id

		# if user is registered and participates in competition
		if(check_registration(self.session, user_id) and check_participating(self.session, user_id)):
			callback()
		else:
			self.bot.send_message(message.chat.id, 'To access the API you have to start participating in the current competition and to be registered, type /register')


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
		self.with_access(message, lambda: buy_ticker(self.session, self.bot, message))
			
			
	# @ACCESS: private
	def sell_ticker(self, message):
		self.with_access(message, lambda: sell_ticker(self.session, self.bot, message))


	# @ACCESS: private
	def send_ranking_data(self, message):
		self.with_access(message, lambda: send_ranking_data(self.session, self.bot, message))


	# @ACCESS: private
	def send_assets_data(self, message):
		self.with_access(message, lambda: send_assets_data(self.session, self.bot, message))