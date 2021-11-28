import models

from sqlalchemy.exc import IntegrityError


# registering new user using from_user id
def register_user(session, bot, message):
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
			bot.send_message(message.chat.id, 'You are successfully registered. Now you can paricipate in weekly competition. To enroll in the current competition type /participate')
		except IntegrityError as err:
			print(err)
			bot.send_message(message.chat.id, 'Something went wrong. Try one more time')