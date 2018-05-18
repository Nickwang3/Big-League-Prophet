from mlbScraper import getPlayersStats, getPlayerIDS, getBirthYear
from salaryScraper import getSalaryData
import io
import csv
import random
from playerAndContract import Player, Contract
import pandas as pd 
import numpy as np
import pandas.io.common


salary_data = pd.read_csv('salary_data/salary_data.csv')

player_IDS = pd.read_csv('playerIDS/IDS.csv', encoding='ANSI')


#creates a list of all players with mlb contracts to be used for machine learning sample data POSSIBLY CHANGE SEARCH METHOD TO USE THIS DICTIONARY FASTER
def getActivePlayerDict():

	dict_of_active_players = {}

	list_of_active_players = []
	list_of_player_teams = []

	#creating list of players as keys
	for playerName in salary_data.Name.values:

		list_of_active_players.append(playerName)

	#creating list of player's teams 
	for team in salary_data.Team.values:

		list_of_player_teams.append(team)

	count = 0
	for player in list_of_active_players:

		dict_of_active_players[player] = list_of_player_teams[count]
		count+=1

	return dict_of_active_players

#grabs a random active player. can be used as sample data for machine learning
def getRandomPlayer():

	dicts = getActivePlayerDict()

	getRandomPlayer.player, getRandomPlayer.team = random.choice(list(dicts.items()))
	
	return getRandomPlayer.player, getRandomPlayer.team




#creates a player object
def createPlayer(playerName, teamAbbrev):

	df = []

	#check if player entered is in data base. Must check multiple name sources because sometimes there is variance
	if playerName in player_IDS.espn_name.values and teamAbbrev in player_IDS.mlb_team.values:

		df = player_IDS[player_IDS.espn_name==playerName]

	elif playerName in player_IDS.mlb_name.values and teamAbbrev in player_IDS.mlb_team.values:

		df = player_IDS[player_IDS.mlb_name==playerName]

	elif playerName in player_IDS.cbs_name.values and teamAbbrev in player_IDS.mlb_team.values:

		df = player_IDS[player_IDS.cbs_name==playerName]
	else:
		print("player not found")
		return -1

	#checking if there are players with the same name
	if len(df.index) > 1:
		for row in df.itertuples(index=True, name='Pandas'):

			if str(getattr(row, "mlb_team"))==teamAbbrev:
				espn_id =  str(int(getattr(row, "espn_id")))

	else:
		for row in df.itertuples(index=True, name='Pandas'):

			espn_id = str(int(getattr(row, "espn_id")))





	#now grab salary data for player
	salary_df = []

	if playerName in salary_data.Name.values:

		salary_df = salary_data[salary_data.Name.values==playerName]

	else:
		print("player not found (Possibly changed teams recently)")
		return -1



	#again checking for multiple players with the same name
	if len(salary_df.index) > 1:
		for row in salary_df.itertuples(index=True, name='Pandas'):

			if str(getattr(row, "Team"))==teamAbbrev:

				sign_year = getattr(row, "Years_Signed")
				years_active = getattr(row, "Years_Active")
				length = getattr(row, "Contract_Length")
				total_value = getattr(row, "int_value")
				avg_value = getattr(row, "int_annual")
				current_salary = getattr(row, "int_salary")
				position = getattr(row, "POS")

	else:
		for row in salary_df.itertuples(index=True, name='Pandas'):

				sign_year = getattr(row, "Years_Signed")
				years_active = getattr(row, "Years_Active")
				length = getattr(row, "Contract_Length")
				total_value = getattr(row, "int_value")
				avg_value = getattr(row, "int_annual")
				current_salary = getattr(row, "int_salary")
				position = getattr(row, "POS")



	#now grab player stats 
	player_file_name = playerName.replace(" ", "-")
	try:
		player_stats = pd.read_csv('baseballStatsPlayers/' + player_file_name + ".csv")
	except (FileNotFoundError, TypeError, pandas.io.common.EmptyDataError):
		# print("That player does not exist or has no stats prior to signing")
		return -1


	try:
		stats_before_signing = player_stats[(player_stats[['SEASON']] < sign_year).all(axis=1)]
	except KeyError:
		stats_before_signing = player_stats[(player_stats[['YEAR']] < sign_year).all(axis=1)]


	
	age_at_signing = sign_year - getBirthYear('http://www.espn.com/mlb/player/stats/_/id/' + espn_id + "/" + playerName)

	if getBirthYear('http://www.espn.com/mlb/player/stats/_/id/' + espn_id + "/" + playerName) == -1:
		age_at_signing = None




	#create the contract object
	contract = Contract(length, years_active, total_value, current_salary, avg_value, sign_year)

	player = playerName+teamAbbrev

	#creating the player object
	player = Player(espn_id, playerName, teamAbbrev, player_stats, stats_before_signing, position, contract, age_at_signing)



	return player


