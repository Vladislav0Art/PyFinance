from models import User, Asset, Transaction

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



def buy_ticker(session, bot, message):
	user_id = message.from_user.id
	params = get_params_from_command(message.text)

	# if validation is failed
	if (not validate_params(params)):
		return bot.send_message(message.chat.id, 'Incorrect command. Pass ticker and amount of shares you want to purchase')

	# retrieving ticker and amount
	ticker, amount = params
	amount = int(amount)

	# if amount is zero
	if(amount == 0):
		return bot.send_message(message.chat.id, 'The minimum amount of shares you can buy is 1')

	# if ticker does not exist
	if (not MarketService.does_ticker_exist(ticker)):
		return bot.send_message(message.chat.id, 'Provided ticker is not supported on PyFinance Stock Market')

	# getting ask price for ticker
	ask_price = MarketService.get_ticker_ask_price(ticker) or 157.12


	# if ticker is not being traded now
	# if (ask_price is None):
	# 	return bot.send_message(message.chat.id, 'Ticker is not being traded now')


	# searching for user in db
	user = User.find_by_id(session, user_id)
	
	# counting total price
	total_price = round(ask_price * amount, 2)

	# if user does not have enough usd to buy stocks
	if (user.usd_amount < total_price):
		return bot.send_message(
			message.chat.id,
			"Your USD account is less then required for buying:\n\n<b>Account:</b> {usd_amount}$\n<b>Required:</b> {total_price}$"
			.format(usd_amount=user.usd_amount, total_price=total_price),
			parse_mode='HTML'
		)

	# searching for asset with provided ticker in user instance
	asset = User.get_asset_by_competition_id_and_ticker({
		'user': user, 
		'competition_id': CompetitionService.competition_id, 
		'ticker': ticker,
	})


	try:
		# if user has a ticker then update asset in db
		if (asset):
			Asset.update_ticker_by_user_and_competition_id(session, {
				'user_id': user_id,
				'ticker': asset.ticker,
				'competition_id': CompetitionService.competition_id,
				'query': {
					'amount': asset.amount + amount
				}
			})
		# if user does not have an asset with provided ticker
		else:
			# creating asset instance
			asset = Asset.create_asset_instance({
				'ticker': ticker,
				'ticker_name': MarketService.get_ticker_name(ticker),
				'amount': amount,
				'user_id': user_id,
				'competition_id': CompetitionService.competition_id
			})

			# adding asset in session
			session.add(asset)

			# creating transaction
			transaction = Transaction.create_transaction_instance({
				'user_id': user_id, 
				'competition_id': CompetitionService.competition_id, 
				'type': 'buying', 
				'ticker': asset.ticker, 
				'amount': asset.amount, 
				'ticker_price': ask_price,
			})

			# adding transaction in session
			session.add(transaction)

			# saving data in db
			session.commit()


		# updating user's usd amount
		current_usd_amount = round(user.usd_amount - total_price, 2)
		User.update_by_id(session, {
			'id': user_id,
			'query': {
				'usd_amount': current_usd_amount
			}
		})

		user = User.find_by_id(session, user_id)
		print('USER ASSETS: ', user.assets)

		bot.send_message(
			message.chat.id, 
			"<strong>Successful transaction:</strong>\n\n<b>Purchased amount of shares:</b> {amount}\n<b>Price for each:</b> {price_each}$\n<b>Total price:</b> {total_price}$\n<b>Current USD account:</b> {current_usd}$"
			.format(
				amount=amount,
				price_each=ask_price,
				total_price=total_price,
				current_usd=current_usd_amount
			),
			parse_mode='HTML'
		)

	except Exception as err:
		print(err)
		bot.send_message(message.chat.id, 'Error occured on the server side, please, try again')