import models
from config import config

from sqlalchemy.exc import IntegrityError


# setting is_participating to true and assign 1000$ to the account
def enroll_user_in_competition(session, bot, message):
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