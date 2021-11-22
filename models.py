import datetime

from sqlalchemy import select
from sqlalchemy import (Column, Integer, String, DateTime, Boolean)
from sqlalchemy.schema import UniqueConstraint

from config import db



class User(db.Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	first_name = Column(String, nullable=False)
	last_name = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow)

	@classmethod
	def create_user(cls, user_data):
		if('id' not in user_data or 'first_name' not in user_data or 'last_name' not in user_data):
			raise ValueError('All fields must be filled')

		return cls(**user_data)		

	
	@classmethod
	def get_user_by_id(cls, session, id):
		return session.execute(
			select(cls).where(cls.id == id)
		)