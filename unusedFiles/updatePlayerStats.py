import pandas as pd 
import numpy as np
from mlbScraper import getPlayersStats, getPlayerIDS, getBirthYear
import io
import csv
import random
from playerAndContract import Player, Contract
import pandas.io.common


#creating panda data frames for player id search and salary data search
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



#below are the get methods for retrieving data from the data bases
#these will be called to retrive data in the easiest way possible

#gets the id of a specific player
def getPlayerID(playerName, teamAbbrev):

	df = []
	#check if player entered is in data base. Must check multiple name sources because sometimes there is variance
	if playerName in player_IDS.espn_name.values and teamAbbrev in player_IDS.mlb_team.values:

		df = player_IDS[player_IDS.espn_name==playerName]

	elif playerName in player_IDS.mlb_name.values and teamAbbrev in player_IDS.mlb_team.values:

		df = player_IDS[player_IDS.mlb_name==playerName]

	elif playerName in player_IDS.cbs_name.values and teamAbbrev in player_IDS.mlb_team.values:

		df = player_IDS[player_IDS.cbs_name==playerName]
	else:
		print("player not found (Possibly changed teams recently)")
		return -1

	#checking if there are players with the same name
	if len(df.index) > 1:
		for row in df.itertuples(index=True, name='Pandas'):

			if str(getattr(row, "mlb_team"))==teamAbbrev:
				return str(int(getattr(row, "espn_id")))
	else:
		for row in df.itertuples(index=True, name='Pandas'):

			return str(int(getattr(row, "espn_id")))


# gets the players standard stats  (DATAFRAME)
def getStats(playerName, teamAbbrev):

	espn_id = getPlayerID(playerName, teamAbbrev)
	getPlayersStats(espn_id, playerName)

	player_file_name = playerName.replace(" ", "-") + "#" + espn_id

	#looks for player stats file in folder
	try:
		player_stats = pd.read_csv('baseballStatsPlayers/' + player_file_name + ".csv")
	except (FileNotFoundError, TypeError, pandas.io.common.EmptyDataError):
		# print("That player does not exist or has no stats prior to signing")
		return -1

	return player_stats


#creates all player stats files
def createAllPlayerStats():

	playerDict = getActivePlayerDict()

	for playerName in playerDict:
		team = playerDict[playerName]
		try:
			getStats(playerName, team)
		except:
			pass






#updates all players stats
def main():

	getPlayerIDS()
	getActivePlayerDict()
	createAllPlayerStats()
main()