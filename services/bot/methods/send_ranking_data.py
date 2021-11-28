# services
from services.competition.CompetitionService import CompetitionService



def get_params_from_command(command):
	# retrieving params passed after command
	params = command.split(' ')[1::]
	return params



def validate_params(params):
	result = False
	# checking if there 2 params and second one is integer
	if(len(params) == 1 and params[0].isdigit()):
		result = True
	
	return result



def send_ranking_data(session, bot, message):
	user_id = message.from_user.id
	params = get_params_from_command(message.text)

	# if params are passed
	if (len(params)):
		# if validation is failed
		if (not validate_params(params)):
			return bot.send_message(message.chat.id, 'Incorrect command. Pass a correct competition id')

		# retrieving competition id
		competition_id = params[0]

		global_ranking_message = CompetitionService.create_ranking_table_by_competition_id(competition_id)

		# data of provided competition not found
		if (global_ranking_message is None):
			return bot.send_message(message.chat.id, 'Data for the provided competition not found')

		# creating personal ranking
		personal_rank_message = CompetitionService.create_personal_rank_message({
			'user_id': user_id,
			'competition_id': competition_id
		})

		# sending global rank
		bot.send_message(message.chat.id, global_ranking_message, parse_mode='HTML')
		# sending personal rank 
		if(personal_rank_message):
			bot.send_message(message.chat.id, personal_rank_message, parse_mode='HTML')


	# if current ranking data is requested
	else:
		# geetting ranks
		sorted_ranks = CompetitionService.calculate_rankings()
		
		# creating global ranking
		ranking_message = CompetitionService.create_ranking_table_for_current_competition(sorted_ranks)
		
		# creating personal ranking
		personal_rank_message = CompetitionService.create_personal_rank_message({
			'user_id': user_id,
			'competition_id': CompetitionService.competition_id
		})

		# sending global rank
		bot.send_message(message.chat.id, ranking_message, parse_mode='HTML')
		# sending personal rank 
		if(personal_rank_message):
			bot.send_message(message.chat.id, personal_rank_message, parse_mode='HTML')