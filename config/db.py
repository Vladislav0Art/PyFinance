from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import keys

# all models should inherit from Base to be processed by SQLAlchemy
Base = declarative_base()

ENGINE = create_engine(keys.DATABASE)

Base.metadata.create_all(ENGINE)

Session = sessionmaker(ENGINE)