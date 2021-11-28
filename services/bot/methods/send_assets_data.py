from models import Asset, Transaction, User

# services
from services.competition.CompetitionService import CompetitionService




def send_assets_data(session, bot, message):
	user_id = message.from_user.id
	user = User.find_by_id(session, user_id)		
	
	assets = Asset.retrieve_by_user_and_competition_id(session, {
		'user_id': user_id,
		'competition_id': CompetitionService.competition_id
	})

	response = '<strong>Your assets:</strong>\n\n<b>Current USD account:</b> {usd}$\n\n'.format(usd=user.usd_amount)

	asset_template = '{number}) <b>Ticker:</b> {ticker}\n<b>Name:</b> {ticker_name}\n<b>Amount:</b> {amount}\n\n'
	
	buying_transaction_template = '<b>Created at:</b> {created_at}\n<b>Amount of shares:</b> {amount}\n<b>Ticker price:</b> {ticker_price}$\n<b>Total price:</b> {total_price}$\n<b>Current profit USD:</b> {profit_usd}$\n<b>Current profit %:</b> {profit_percent}%\n\n'

	selling_transaction_template = '<b>Created at:</b> {created_at}\n<b>Amount of shares:</b> {amount}\n<b>Ticker price:</b> {ticker_price}$\n<b>Total price:</b> {total_price}$\n\n'

	index = 0
	for asset in assets:
		index += 1
		response += asset_template.format(
			number=index,
			ticker=asset.ticker.upper(),
			ticker_name=asset.ticker_name,
			amount=asset.amount
		)

		response += '<b>Transactions with {ticker}:</b>\n\n'.format(ticker=asset.ticker.upper())

		transactions = Transaction.find_by_user_competition_ids_and_ticker(session, {
			'user_id': user_id,
			'competition_id': CompetitionService.competition_id,
			'ticker': asset.ticker,
		})

		# buying and selling transaction messages
		buying_transaction_message = '<b>Buying transactions:</b>\n\n'
		selling_transaction_message = '<b>Selling transactions:</b>\n\n'

		had_buying_transactions = False
		had_selling_transactions = False

		for transaction in transactions:
			# buying type
			if(transaction.type == 'buying'):
				had_buying_transactions = True
				profit_usd, profit_percent = Transaction.estimate_profit_of_buying_transaction(transaction)

				current_transaction_message = buying_transaction_template.format(
					created_at=transaction.created_at,
					type=transaction.type,
					amount=transaction.amount,
					ticker_price=transaction.ticker_price,
					total_price=transaction.ticker_price * transaction.amount,
					profit_usd=profit_usd, 
					profit_percent=profit_percent,
				)

				buying_transaction_message += current_transaction_message

			# selling type
			else:
				had_selling_transactions = True
				current_transaction_message = selling_transaction_template.format(
					created_at=transaction.created_at,
					type=transaction.type,
					amount=transaction.amount,
					ticker_price=transaction.ticker_price,
					total_price=transaction.ticker_price * transaction.amount,
				)

				selling_transaction_message += current_transaction_message

		if(had_buying_transactions):
			response += buying_transaction_message
		if(had_selling_transactions):
			response += selling_transaction_message


	total_account = round(user.usd_amount + Asset.calculate_market_price_of_assets(assets), 2)
	
	response += '<b>Total account:</b> {total_account}$'.format(total_account=total_account)

	# sending message
	bot.send_message(message.chat.id, response, parse_mode='HTML')