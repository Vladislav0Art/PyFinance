import datetime

from sqlalchemy import ForeignKey, desc
from sqlalchemy import (Column, Integer, String, DateTime, Boolean, Float)
from sqlalchemy.orm import relationship

# config
from config import config

# services
from services.market.MarketService import MarketService



# checks in any fields are missing
def validate_fields(required_fields, data):
	result = True

	for field in required_fields:
		if field not in data:
			result = False
			break

	return result



# User model
class User(config.Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	username = Column(String, nullable=False, unique=True)
	is_participating = Column(Boolean, default=False)
	usd_amount = Column(Float, default=0)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow)


	def __repr__(self):
		return "<Class User: id='{id}', username='{username}', usd_amount='{usd_amount}'>" \
			.format(
				id=self.id, 
				username=self.username,
				usd_amount=self.usd_amount
			)
	

	# returns new user instance
	@classmethod
	def create_user_instance(cls, user_data):
		# if any field is not specified
		required_fields = ['id', 'first_name', 'last_name', 'username']

		# if some fields are missing
		if not validate_fields(required_fields, user_data):
			raise ValueError('All fields must be filled')

		# creating user instance
		return cls(**user_data)



	# updating passed field of user matched by id
	@classmethod
	def update_by_id(cls, session, params):
		id = params['id']
		update_query = params['query']

		# updating user fields
		session.query(cls)\
			.filter(cls.id == id)\
			.update({
				**update_query,
				'updated_at': datetime.datetime.utcnow()
			})
		# committing changes
		session.commit()

	
	# searching for user by id 
	@classmethod
	def find_by_id(cls, session, id):
		return session.query(cls).filter(cls.id == id).first()

	
	# returns asset by ticker if user has one, otherwise returns None
	@classmethod
	def get_asset_by_competition_id_and_ticker(cls, params):
		user = params['user']
		competition_id = params['competition_id']
		provided_ticker = params['ticker']

		# lowercasing provided ticker
		provided_ticker = provided_ticker.lower()

		found_asset = None
		
		# searching for ticker in user assets with current competition id
		for asset in user.assets:
			print(asset)

			print(provided_ticker, competition_id)

			if (asset.ticker == provided_ticker) and (asset.competition_id == competition_id):
				found_asset = asset
				print(found_asset)
				break
		
		print(found_asset)
		return found_asset



	# retrieving all users
	@classmethod
	def retrieve_all(cls, session):
		return session.query(cls).all()




# Asset model
class Asset(config.Base):
	__tablename__ = 'assets'

	id = Column(Integer, primary_key=True)
	ticker = Column(String, nullable=False)
	ticker_name = Column(String, nullable=False)
	amount = Column(Integer, default=0)
	competition_id = Column(Integer, nullable=False)

	user_id = Column(Integer, ForeignKey('users.id'))


	def __repr__(self):
		return "<Class Asset: id='{id}', user_id='{user_id}' ticker='{ticker}' competition_id='{competition_id}'>"\
			.format(
				id=self.id, 
				ticker=self.ticker,
				user_id=self.user_id,
				competition_id=self.competition_id
			)


	# @classmethod
	# def find_assets_by_user_id(cls, session, user_id):
	# 	return session.query(cls).filter(cls.user_id == user_id).all()

	@classmethod
	def create_asset_instance(cls, asset_data):
		required_fields = ['ticker', 'ticker_name', 'amount', 'user_id', 'competition_id']

		# if any fields are missing
		if not validate_fields(required_fields, asset_data):
			raise ValueError('All fields must be filled')

		# lowercasing ticker
		asset_data['ticker'] = asset_data['ticker'].lower()

		return cls(**asset_data)



	@classmethod
	def update_ticker_by_user_and_competition_id(cls, session, params):
		# updating ticker fields
		session\
			.query(cls)\
			.filter(cls.user_id == params['user_id'], 
					cls.ticker == params['ticker'],
					cls.competition_id == params['competition_id'])\
			.update({
				**params['query']
			})
		# committing changes
		session.commit()


	@classmethod
	def retrieve_by_user_and_competition_id(cls, session, params):
		user_id = params['user_id']
		competition_id = params['competition_id']

		return session\
			.query(cls)\
			.filter(cls.user_id == user_id,
					cls.competition_id == competition_id)\
			.all()

	
	
	@classmethod
	def calculate_market_price_of_assets(cls, assets):
		market_price_of_assets = 0

		for asset in assets:
			price = MarketService.get_ticker_ask_price(asset.ticker)
			
			if(price is None):
				price = MarketService.get_last_price(asset.ticker)

			market_price_of_assets += asset.amount * price

		return market_price_of_assets
			





# UserRank model
class UserRank(config.Base):
	__tablename__ = 'user-ranks'

	id = Column(Integer, primary_key=True)
	competition_id = Column(Integer, nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'))
	username = Column(String, nullable=False)
	place = Column(Integer, nullable=False)
	total_account = Column(Float, nullable=False)


	def __repr__(self):
		return "<Class UserRank: id='{id}', user_id='{user_id}' competition_id='{competition_id}'>"\
			.format(
				id=self.id, 
				user_id=self.user_id,
				competition_id=self.competition_id,
			)


	@classmethod
	def create_user_rank_instance(cls, user_rank_data):
		required_fields = ['user_id', 'username', 'place', 'competition_id']

		# if some fields are not provided
		if (not validate_fields(required_fields, user_rank_data)):
			raise ValueError('All fields must be filled')

		return cls(**user_rank_data)


	@classmethod
	def find_by_user_and_competition_id(cls, session, params):
		user_id = params['user_id']
		competition_id = params['competition_id']

		return session\
						.query(cls)\
						.filter(cls.user_id == user_id, 
								cls.competition_id == competition_id)\
						.first()



	@classmethod
	def find_by_competition_id(cls, session, competition_id):
		return session\
							.query(cls)\
							.filter(cls.competition_id == competition_id)\
							.order_by(desc(cls.total_account))\
							.all()



# specifying relationships between models

# User - Asset
User.assets = relationship('Asset', order_by=Asset.competition_id, back_populates='user')
Asset.user = relationship('User', back_populates='assets')

# User - UserRank
User.ranks = relationship('UserRank', order_by=UserRank.competition_id, back_populates='user')
UserRank.user = relationship('User', back_populates='ranks')