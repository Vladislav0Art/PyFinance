import datetime

from sqlalchemy import select
from sqlalchemy import (Column, Integer, String, DateTime, Boolean)

from config import config



class User(config.Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	username = Column(String, nullable=False, unique=True)
	is_participating = Column(Boolean, default=False)
	usd_amount = Column(Integer, default=0)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow)


	def __repr__(self):
		return '<Class User> id: {id}; username: {username}' \
			.format(
				id=self.id, 
				username=self.username
			)
	

	# returns new user instance
	@classmethod
	def create_user_instance(cls, user_data):
		# if any field is not specified
		fields = ['id', 'first_name', 'last_name', 'username']

		# if some fields are missing
		for field in fields:
			if field not in user_data:
				raise ValueError('All fields must be filled')
		
		# creating user instance
		user = dict()
		for field in fields:
			user[field] = user_data[field]

		return cls(**user)


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

	
	@classmethod
	def find_by_id(cls, session, id):
		return session.query(cls).filter(cls.id == id).first()

	@classmethod
	def retrieve_all(cls, session):
		return session.query(cls).all()