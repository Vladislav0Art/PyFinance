import datetime

from sqlalchemy import select
from sqlalchemy import (Column, Integer, String, DateTime)

from config import config



class User(config.Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow)

	def __repr__(self):
		return '<Class User> id: {id}; first_name: {first_name}; last_name: {last_name}' \
			.format(
				id=self.id, 
				first_name=self.first_name, 
				last_name=self.last_name
			)

	@classmethod
	def create_user(cls, user_data):
		# if any field is not specified
		if('id' not in user_data or 'first_name' not in user_data or 'last_name' not in user_data):
			raise ValueError('All fields must be filled')
		
		user = {
			'id': user_data['id'],
			'first_name': user_data['first_name'],
			'last_name': user_data['last_name']
		}

		return cls(**user)

	
	@classmethod
	def get_user_by_id(cls, session, id):
		return session.execute(
			select(cls).where(cls.id == id)
		)

	@classmethod
	def get_users(cls, session):
		return session.query(cls).all()