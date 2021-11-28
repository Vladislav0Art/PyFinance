# Welcome to PyFinance bot - a trading competition platform created as a Python project by HSE student Artuhov Vladislav @Vladislav0Art 


### The rules are as follows:
  1) Each week at Sunday **2000$** is assigned to your account.
  2) You have exactly one week of trading, next Sunday is the deadline.
  3) After deadline top 10 players will be Competition Winners.
  4) Then it starts over again, as simple as that.
  
**If you want to know about supported commands type `/help`**

### Supported commands:
  1) `/start` - show basic information about the project.

  2) `/register` - registers new user (required to have access to most of the commands, **first command you need to type**).

  3) `/participate` - sets a user as a participant (required to have access to trading).

  4) `/market [ticker]` - shows a list of avaliable stocks on the PyFinance trading platform. If ticker is specified shows detailed info about the ticker; ticker can be typed in either lower or upper case. Example: `/market AAPL`.

  5) `/assets` - shows all user assets and transactions made during current competition.

  6) `/ranking [competition id]` - if [competition id] is not provided shows results of the current competition, otherwise shows results of the competition with the provided id. Example: `/ranking 0`.

  7) `/buy [stock ticker] [amount]` - buys a stock at specified amount. Ticker can be typed in either lower and upper cases. Example: `/buy AAPL 3`.

  8) `/sell [stock ticker] [amount]` - sells a stock at specified amount. Ticker can be typed in either lower and upper cases. Example: `/sell AAPL 3`.

### Dependencies:
  1) `pyTelegramBotAPI`   4.2.0
  2) `SQLAlchemy`         1.4.27

### Launching the program:
  1) Type from the project folder: `python main.py`
  2) Open telegram and search for bot `@py_finance_bot`


#### P.S.1: 
The codebase for this project is **complete mess**, please **do not judge the author**, he has spent on this project **too little amount of time** to make it decent `:(`

#### P.S.2:
Warning: `**bugs**` and `**undesired effects**` may occur. Even author has no idea that might happen...