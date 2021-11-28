from models import Asset, User

from services.market.MarketService import MarketService
from services.competition.CompetitionService import CompetitionService


def get_params_from_command(command):
	# retrieving params passed after command
	params = command.split(' ')[1::]
	return params



def validate_params(params):
	result = False
	# checking if there 2 params and second one is integer
	if(len(params) == 2 and params[1].isdigit()):
		result = True
	
	return result



def sell_ticker(session, bot, message):
	user_id = message.from_user.id
	params = get_params_from_command(message.text)

	# if validation is failed
	if (not validate_params(params)):
		return bot.send_message(message.chat.id, 'Incorrect command. Pass ticker and the amount of shares you want to sell')

	# retrieving ticker and amount
	ticker, amount = params
	amount = int(amount)

	# if amount is zero
	if (amount == 0):
		return bot.send_message(message.chat.id, 'The minimum amount of shares you can sell is 1')

	# if ticker does not exist
	if (not MarketService.does_ticker_exist(ticker)):
		return bot.send_message(message.chat.id, 'Provided ticker is not supported on PyFinance Stock Market')


	# searching for user in db
	user = User.find_by_id(session, user_id)

	# searching for asset with provided ticker in user instance
	asset = User.get_asset_by_competition_id_and_ticker({
		'user': user,
		'competition_id': CompetitionService.competition_id, 
		'ticker': ticker,
	})

	# if user does not have provided asset
	if (not asset or asset.amount <= 0):
		return bot.send_message(message.chat.id, 'You do not have any shares of the provided ticker')

	# if user's amount of shares is less than passed amount
	if (asset.amount < amount):
		return bot.send_message(
			message.chat.id, 
			"Your amount of shares is less than you have provided for selling:\n\n<b>Your amount:</b> {user_amount_of_shares}\n<b>Provided amount for selling:</b> {provided_amount_of_shares}"
			.format(
				user_amount_of_shares=asset.amount,
				provided_amount_of_shares=amount
			),
			parse_mode='HTML'
		)

	# getting ask price for ticker
	bid_price = MarketService.get_ticker_bid_price(ticker) or 157.12

	# if ticker is not being traded now
	# if (bid_price is None):
	# 	return bot.send_message(message.chat.id, 'Ticker is not being traded now')

	try:
		# updating asset in db
		Asset.update_ticker_by_user_and_competition_id(session, {
			'user_id': user_id,
			'ticker': ticker,
			'competition_id': CompetitionService.competition_id,
			'query': {
				'amount': asset.amount - amount
			}
		})

		# current account usd and total_sale_price
		total_sale_price = bid_price * amount
		current_account_usd = user.usd_amount + total_sale_price

		# updating user usd account
		User.update_by_id(session, {
			'id': user_id,
			'query': {
				'usd_amount': current_account_usd
			}
		})

		# sending response
		bot.send_message(
			message.chat.id, 
			"<strong>Successful transaction:</strong>\n\n<b>Sold amount of shares:</b> {amount}\n<b>Price for each:</b> {price_each}$\n<b>Total price:</b> {total_price}$\n<b>Current USD account:</b> {current_usd}$"
			.format(
				amount=amount,
				price_each=bid_price,
				total_price=total_sale_price,
				current_usd=current_account_usd
			),
			parse_mode='HTML'
		)

	except Exception as err:
		print(err)
		bot.send_message(message.chat.id, 'Error occured on the server side, please, try again')
