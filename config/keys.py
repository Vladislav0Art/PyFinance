import os

# constants
TELEGRAM_BOT_API_KEY = os.environ.get('TELEGRAM_BOT_API_KEY', '2139469664:AAHq190nHx2FNDSnSND8TtSXaTQ5xL5lcUU')
DATABASE = os.environ.get('DATABASE', 'sqlite:///pyfinance.db')

