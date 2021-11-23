import os

from sqlalchemy.ext.declarative import declarative_base


# Database configuration
DATABASE = os.environ.get('DATABASE', 'sqlite:///pyfinance.db')
# all models should inherit from Base to be processed by SQLAlchemy
print('creating Base')
Base = declarative_base()


# Telegram constants
TELEGRAM_BOT_API_KEY = os.environ.get('TELEGRAM_BOT_API_KEY', '2139469664:AAHq190nHx2FNDSnSND8TtSXaTQ5xL5lcUU')


# App constants
COMPETITION_DEFAULT_USD_AMOUNT = 1000