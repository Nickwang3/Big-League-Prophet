import pandas as pd 
import numpy as np
from baseballReferenceScrape import getPlayersStats, getPlayerIDS
from salaryScraper import getSalaryData
import io
import csv


#creating panda data frames for player id search and salary data search
salary_data = pd.read_csv('salary_data/salary_data.csv')

player_IDS = pd.read_csv('playerIDS/IDS.csv', encoding='ANSI')


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
		salary = int(salary[2:].replace(",", ""))

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

# gets the players stats from the years prior to the signing of the newest contract (DATAFRAME)
def getStatsBeforeSigning(playerName, teamAbbrev):

	bref_id = getPlayerID(playerName, teamAbbrev)
	getPlayersStats(bref_id)

	full_name = playerName.replace(" ", "")
	player_stats = pd.read_csv('battingStatsPlayers/' + bref_id + teamAbbrev + ".csv")

	year_signed = getContractSignYear(playerName) - 1

	indx = player_stats[player_stats['Year'].astype(int)==year_signed].index.item()

	adjusted_stats = player_stats.ix[~(player_stats['Year'] > year_signed)]
		
	return adjusted_stats

def main():

	getPlayerIDS()
	getSalaryData()
	user_input_name = input("Enter player who's salary you wish to see: ")
	user_input_team = input("Enter player's team abbreviation (ex - BOS for Boston): ")
	getStatsBeforeSigning(user_input_name, user_input_team)
	print()
	print("Total Contract value:",getTotalContractValue(user_input_name))
	print("Salary Years:",getContractYears(user_input_name))
	print("Year Contract Signed:",getContractSignYear(user_input_name))
	print("Contract length:",getContractLength(user_input_name))
	print("Team:",getPlayerTeam(user_input_name))
	


main()