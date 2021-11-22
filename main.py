import telebot

# order matters: models come first, then comes db module
import models
from config import config
from config import db



with db.Session() as session:

	bot  = telebot.TeleBot(token=config.TELEGRAM_BOT_API_KEY)

	@bot.message_handler(content_types=['text'])
	def reply(message):
		
		id = message.from_user.id
		first_name = message.from_user.first_name
		last_name = message.from_user.last_name

		try:
			user = models.User.create_user({
				'id': id, 
				'first_name': first_name, 
				'last_name': last_name
			})
			session.add(user)
			session.commit()


			bot.send_message(message.chat.id, 'User created: ' + user.first_name + ' ' + user.last_name)
		except Exception as err:
			print(err)
			session.rollback()

	# running
	bot.polling(none_stop=True)

