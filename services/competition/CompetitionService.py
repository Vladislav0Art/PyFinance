from threading import Timer

# models
from models import Asset, User, UserRank

# config
from config import config



# runs callback after passed number of seconds
class SetInterval():
    def __init__(self, sec, callback):
        
        def wrapper():
            self.timer = Timer(sec, wrapper)
            self.timer.start()

            callback()

        self.timer = Timer(sec, wrapper)
        self.timer.start()

    def cancel(self):
        self.timer.cancel()



class CompetitionService():
	competition_id = 0
	interval = None
	session = None
	bot = None

	# starts new competition after provided duration of competitions
	@staticmethod
	def start(params):
		CompetitionService.session = params['session']
		CompetitionService.bot = params['bot']
		CompetitionService.interval = SetInterval(params['duration'], CompetitionService.end_current_competition)


	@staticmethod
	def end_current_competition():
		print('Competition #{id} ended!'.format(id=CompetitionService.competition_id))
		
		# calculating rankings
		sorted_ranks = CompetitionService.calculate_rankings()
		try:
			# saving  rankings
			CompetitionService.save_rankings(sorted_ranks)
		except Exception as err:
			print(err)

		# creating global ranking
		ranking_message = '<strong>PyFinance Competition #{competition_id} has ended!\nCongratulations to the winners of the week!</strong>\n\n'\
					.format(competition_id=CompetitionService.competition_id)
		
		ranking_message += CompetitionService.create_ranking_table_for_current_competition(sorted_ranks)
		
		# sending ranking messages to participated users
		for rank in sorted_ranks:
			personal_rank_message = CompetitionService.create_personal_rank_message({
				'user_id': rank.user.id,
				'competition_id': CompetitionService.competition_id
			})
			
			# sending global rank
			CompetitionService.bot.send_message(rank.user.id, ranking_message, parse_mode='HTML')
			# sending personal rank 
			CompetitionService.bot.send_message(rank.user.id, personal_rank_message, parse_mode='HTML')

		# setting users to default state
		CompetitionService.set_users_to_default_state()
		# increasing current competition id
		CompetitionService.competition_id += 1



	@staticmethod
	def cancel_competitions():
		CompetitionService.interval.cancel()


	@staticmethod
	def create_ranking_table_by_competition_id(competition_id):		
		sorted_ranks = UserRank.find_by_competition_id(CompetitionService.session, competition_id)

		# if none ranks found
		if(len(sorted_ranks) <= 0):
			return None

		message = ''
		rank_template = 'Place <b>#{place}</b>: <b>{username}</b> with <b>{total_account}$</b>\n'

		# creating ranking message
		for place in range(len(sorted_ranks)):
			# if top 10 winners are found
			if (place >= 10):
				break
			
			rank = sorted_ranks[place]
			# inserting info in message
			message += rank_template.format(
				place=place + 1,
				username=rank.username,
				total_account=rank.total_account,
			)
		
		return message


	@staticmethod
	def create_ranking_table_for_current_competition(sorted_ranks):
		message = ''

		rank_template = 'Place <b>#{place}</b>: <b>{username}</b> with <b>{total_account}$</b>\n'

		# creating ranking message
		for place in range(len(sorted_ranks)):
			# if top 10 winners are found
			if (place >= 10):
				break
			
			rank = sorted_ranks[place]
			# inserting info in message
			message += rank_template.format(
				place=place + 1,
				username=rank.username,
				total_account=rank.total_account,
			)
		
		return message


	
	@staticmethod
	def create_personal_rank_message(params):
		user_id = params['user_id']
		competition_id = params['competition_id']

		# searching for user 
		user = User.find_by_id(CompetitionService.session, user_id)
		
		# searchinf for personal rank
		personal_rank = UserRank.find_by_user_and_competition_id(CompetitionService.session, {
			'user_id': user_id,
			'competition_id': competition_id
		})

		# if personal rank not found
		if (not personal_rank):
			return None

		# searching for all assets user had in the end of the competition
		assets = Asset.retrieve_by_user_and_competition_id(CompetitionService.session, {
			'user_id': user.id,
			'competition_id': competition_id
		})


		personal_message = 'You have taken <b>#{place}</b> place with <b>{total_account}$</b>\n\n<strong>Your assets:</strong>\n\n'\
							.format(
								place=personal_rank.place,
								total_account=personal_rank.total_account
							)
		
		asset_template = '<b>Ticker:</b> {ticker}\n<b>Name:</b> {ticker_name}\n<b>Amount:</b> {amount}\n\n'

		# inserting assets info in message
		for asset in assets:
			personal_message += asset_template.format(
				ticker=asset.ticker.upper(),
				ticker_name=asset.ticker_name,
				amount=asset.amount
			)

		# if assets do not exist
		if(len(assets) <= 0):
			personal_message += 'No assets\n'

		return personal_message



	@staticmethod
	# sets usd_amount to default value and is_participating to False
	def set_users_to_default_state():
		CompetitionService.session\
			.query(User)\
			.update({ 
				User.usd_amount: config.COMPETITION_DEFAULT_USD_AMOUNT,
				User.is_participating: False,
			})



	@staticmethod
	def save_rankings(user_rankings):
		for user_rank in user_rankings:
			# adding user rank in session
			CompetitionService.session.add(user_rank)

		CompetitionService.session.commit()



	@staticmethod
	def calculate_rankings() -> list:
		users = User.retrieve_all(CompetitionService.session)

		rankings = []

		# calculating market price of all assets
		for user in users:
			# if user is not participating
			if(not user.is_participating):
				continue
			
			# retrieving all assets of user
			assets = Asset.retrieve_by_user_and_competition_id(CompetitionService.session, {
				'user_id': user.id,
				'competition_id': CompetitionService.competition_id
			})

			# calculating total user account
			total_account = user.usd_amount + Asset.calculate_market_price_of_assets(assets)
			total_account = round(total_account, 2)

			# appending total market price of assets and user id in list
			rankings.append((total_account, user.username, user.id))

		# sorting by total user accounts
		rankings = sorted(rankings)

		try:
			user_ranks_instances = []

			for place in range(len(rankings)):
				# retrieving user id
				total_account, username, user_id = rankings[place]

				# creating new rank instance
				user_rank = UserRank.create_user_rank_instance({
					'user_id': user_id,
					'username': username,
					'place': place + 1,
					'total_account': total_account,
					'competition_id': CompetitionService.competition_id,
				})
				user_ranks_instances.append(user_rank)
			
			return user_ranks_instances

		except Exception as err:
			print(err)
			return []