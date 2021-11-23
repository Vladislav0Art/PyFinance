import telebot
from telebot.types import MessageAutoDeleteTimerChanged

# order matters: models come first, then comes db module
import models
from config import config
from config import db

from sqlalchemy.exc import IntegrityError



with db.Session() as session:
	bot  = telebot.TeleBot(token=config.TELEGRAM_BOT_API_KEY)

	# /start - enrolls user into competition
	@bot.message_handler(commands=['start', 'participate'])
	def enroll_user_in_competition(message):

		id = message.from_user.id

		# searching user in db
		user = models.User.find_by_id(session, id)

		# user is not registered
		if(not user):
			return bot.send_message(message.chat.id, 'You are not registered. Type /register command to register')
		# if user is already participating in competition
		if(user.is_participating):
			return bot.send_message(message.chat.id, 'You are already participating in the current competition')

		try:
			# updating user participating status and setting default usd amount value
			usd_amount = config.COMPETITION_DEFAULT_USD_AMOUNT

			models.User.update_by_id(session, params={
				'id': user.id, 
				'query': {
					'is_participating': True,
					'usd_amount': usd_amount
				}
			})

			# responding with succsess
			bot.send_message(message.chat.id, 'You have been successfully enrolled in the competition. Your starting capital: {usd}$. Take a look at the stock market by typing /market'.format(usd=usd_amount))

		except IntegrityError as err:
			print(err)
			bot.send_message(message.chat.id, 'Something went wrong. Try one more time')


		
	# /register - creates user instance in db
	@bot.message_handler(commands=['register'])
	def register_user(message):

		id = message.from_user.id
		first_name = message.from_user.first_name
		last_name = message.from_user.last_name
		username = message.from_user.username

		# searching user in db
		user = models.User.find_by_id(session, id)

		# if user already registered
		if(user): 
			return bot.send_message(message.chat.id, 'You are already registered. If you want to participate in the current competition type /start or /participate')

		# creating user instance
		user = models.User.create_user_instance({
			'id': id,
			'first_name': first_name,
			'last_name': last_name,
			'username': username
		})
		session.add(user)

		# saving user in db	
		try:
			session.commit()
			bot.send_message(message.chat.id, 'You are successfully registered. Now you can paricipate in weekly competition. To enroll in the current competition type /start or /participate')
		except IntegrityError as err:
			print(err)
			bot.send_message(message.chat.id, 'Something went wrong. Try one more time')



	# running
	bot.polling(none_stop=True)