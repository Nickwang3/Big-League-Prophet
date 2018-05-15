import pandas as pd 
import numpy as np
from baseballReferenceScrape import getPlayersStats, getPlayerIDS
from salaryScraper import getSalaryData
import io
import csv
import random
from playerAndContract import Player, Contract
#creating panda data frames for player id search and salary data search
salary_data = pd.read_csv('salary_data/salary_data.csv')

player_IDS = pd.read_csv('playerIDS/IDS.csv', encoding='ANSI')


#creates a list of all players with mlb contracts to be used for machine learning sample data POSSIBLY CHANGE SEARCH METHOD TO USE THIS DICTIONARY FASTER
def getActivePlayerList():

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

	dicts = getActivePlayerList()

	getRandomPlayer.player, getRandomPlayer.team = random.choice(list(dicts.items()))



#below are the get methods for retrieving data from the data bases
#these will be called to retrive data in the easiest way possible


#gets the id of a specific player
def getPlayerID(playerName, teamAbbrev):

	#check if player entered is in data base
	if playerName in player_IDS.mlb_name.values and teamAbbrev in player_IDS.mlb_team.values:

		indx = player_IDS[player_IDS['mlb_name']==playerName].index.item()
		bref_id = player_IDS.at[indx, 'bref_id']
		bref_id = str(bref_id)

	else:

		print()
		print("Player or team not found")
		return

	return bref_id

#finds the players current team (STRING)
def getPlayerTeam(playerName):

	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		team = salary_data.at[indx, 'Team']
		team = str(team.strip())

	else:

		print()
		print("Player not found")
		return

	return team

#finds the players position
def getPlayerPos(playerName):

	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		position = salary_data.at[indx, 'POS']
		position = str(position.strip())

	else:

		print()
		print("Player not found")
		return

	return position

#return true if pitcher
def isPitcher(playerName):

	pos = getPlayerPos(playerName)

	if pos == 'RP' or pos == 'SP':
		return True 
	return False

#finds a players current salary value for current year in (INTEGER)
def getCurrentYearSalary(playerName):

	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		salary = salary_data.at[indx, 'Salary']
		salary = int(salary[2:].replace(",", ""))

	else:

		print()
		print("Player not found")
		return

	return salary

#finds the contracts total value
def getTotalContractValue(playerName):

	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		salary = salary_data.at[indx, 'Total Value']
		salary = int(salary[1:].replace(",", ""))

	else:

		print()
		print("Player not found")
		return

	return salary

#finds num of years contract is active for (INTEGER)
def getContractLength(playerName):

	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		years = salary_data.at[indx, 'Years']
		indx_paren = years.index("(")
		years = int(years[:indx_paren].strip())

	else:

		print()
		print("Player not found")
		return 

	return years

#gets year span that contract is active in (STRING)
def getContractYears(playerName):
	
	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		years = salary_data.at[indx, 'Years']
		indx_paren = years.index("(")
		indx_close = years.index(")")
		years = years[indx_paren+1:indx_close].strip()

	else:

		print()
		print("Player not found")
		return 

	return years

#gets the year of signing (INTEGER)
def getContractSignYear(playerName):

	#check if player entered is in data base
	if playerName in salary_data.Name.values:

		indx = salary_data[salary_data['Name']==playerName].index.item()
		years = salary_data.at[indx, 'Years']
		indx_paren = years.index("(")
		indx_dash = years.find("-")
		year_signed = int(years[indx_paren+1:indx_dash])


	else:

		print()
		print("Player not found")
		return 

	return year_signed

#finds age at signing contract
def getAgeAtSigning(playerName, teamAbbrev):

	bref_id = getPlayerID(playerName, teamAbbrev)
	getPlayersStats(bref_id)

	full_name = playerName.replace(" ", "")

	#looks for player stats file in folder
	try:
		player_stats = pd.read_csv('baseballStatsPlayers/' + bref_id + teamAbbrev + ".csv")
	except (FileNotFoundError, TypeError):
		print("That player has changed teams recently or does not exist")
		return

	year_signed = getContractSignYear(playerName) - 1

	#checks if player has stats before being signed
	try:
		indx = player_stats[player_stats['Year'].astype(int)==year_signed].index.item()
	except ValueError:
		# print("This player has no stats from previous years")
		return

	#used for age analysis
	age = player_stats.loc[indx, 'Age']

	return age


# gets the players standard stats  (DATAFRAME)
def getStats(playerName, teamAbbrev):

	bref_id = getPlayerID(playerName, teamAbbrev)
	getPlayersStats(bref_id)

	full_name = playerName.replace(" ", "")

	#looks for player stats file in folder
	try:
		player_stats = pd.read_csv('baseballStatsPlayers/' + bref_id + teamAbbrev + ".csv")
	except (FileNotFoundError, TypeError):
		print("That player has changed teams recently or does not exist")
		return

	year_signed = getContractSignYear(playerName) - 1

	#checks if player has stats before being signed
	try:
		indx = player_stats[player_stats['Year'].astype(int)==year_signed].index.item()
	except ValueError:
		print("This player has no stats from previous years")
		return

	#cuts off excess stats that are not needed and error filled stats (different based on pitcher or hitter)
	if isPitcher(playerName) == False:
		trimmed_stats = player_stats.iloc[0:, 0:30]
	if isPitcher(playerName) == True:
		trimmed_stats = player_stats.iloc[0:, 0:35]

	return trimmed_stats

# gets the players stats from the years prior to the signing of the newest contract (DATAFRAME)
def getStatsBeforeSigning(playerName, teamAbbrev):

	bref_id = getPlayerID(playerName, teamAbbrev)
	getPlayersStats(bref_id)

	full_name = playerName.replace(" ", "")

	#looks for player stats file in folder
	try:
		player_stats = pd.read_csv('baseballStatsPlayers/' + bref_id + teamAbbrev + ".csv")
	except (FileNotFoundError, TypeError):
		print("That player has changed teams recently or does not exist")
		return

	year_signed = getContractSignYear(playerName) - 1

	#checks if player has stats before being signed
	try:
		indx = player_stats[player_stats['Year'].astype(int)==year_signed].index.item()
	except ValueError:
		print("This player has no stats from previous years")
		return

	adjusted_stats = player_stats.ix[~(player_stats['Year'] > year_signed)]

	#cuts off excess stats that are not needed and error filled stats (different based on pitcher or hitter)
	if isPitcher(playerName) == False:
		trimmed_stats = adjusted_stats.iloc[0:, 0:30]
	if isPitcher(playerName) == True:
		trimmed_stats = adjusted_stats.iloc[0:, 0:35]

	return trimmed_stats


#will only be used inside playerObjectFunction
def createContractObject(playerName, teamAbbrev):

	length = getContractLength(playerName)
	years = getContractYears(playerName)
	total_value = getTotalContractValue(playerName)
	current_salary = getCurrentYearSalary(playerName)
	sign_year = getContractSignYear(playerName)
	age_at_signing = getAgeAtSigning(playerName, teamAbbrev)

	contract = Contract(length, years, total_value, current_salary, sign_year, age_at_signing)

	return contract


#creates an mlb player object 
def createPlayerObject():

	getRandomPlayer()
	name = getRandomPlayer.player
	team = getRandomPlayer.team
	free_agent = False
	stats = getStats(name, team)
	stats_before_signing = getStatsBeforeSigning(name, team)
	position = getPlayerPos(name)

	#calls the contract method to create contract object for player
	contract = createContractObject(name, team)


	player = name+team
	#creating the player object
	player = Player(name, team, free_agent, stats, stats_before_signing, position, contract)

	return player




def main():

	getPlayerIDS()
	getSalaryData()
	getActivePlayerList()

	#below is user input program (commented out) vs an automated random selection of a player


	player1 = createPlayerObject()
	print(player1.name)
	print(player1.stats)
	print(player1.free_agent)
	print(player1.contract.length)
	print(player1.contract.total_value)
	print(player1.contract.age_at_signing)
	


main()