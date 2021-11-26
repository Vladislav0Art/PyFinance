from services.bot.methods.enroll_user_in_competition import enroll_user_in_competition
from services.bot.methods.register_user import register_user


class BotService():
	def __init__(self, session, bot):
		self.session = session
		self.bot = bot

	def enroll_user_in_competition(self, message):
		enroll_user_in_competition(self.session, self.bot, message)

	def register_user(self, message):
		register_user(self.session, self.bot, message)