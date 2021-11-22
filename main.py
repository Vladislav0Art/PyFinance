import os
import telebot

from config import keys, db
import models


with db.Session() as session:

	bot  = telebot.TeleBot(token=keys.TELEGRAM_BOT_API_KEY)

	@bot.message_handler(content_types=['text'])
	def reply(message):

		id = message.from_user.id
		first_name = message.from_user.first_name
		last_name = message.from_user.last_name
		
		print(id, first_name, last_name)

		user_data = {
			
		}

		models.User.create_user(
			session, 
		)

		bot.send_message(message.chat.id, message.text)


	# running
	bot.polling(none_stop=True)

