from models import User

# if user registered returns user object, otherwise None
def check_registration(session, user_id):
	user = User.find_by_id(session, user_id)
	return user


# if user exists and user participates in competition returns True, otherwise False
def check_participating(session, user_id):
	user = User.find_by_id(session, user_id)
	return user and user.is_participating