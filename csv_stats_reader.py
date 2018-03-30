import pandas as pd 
import numpy as np
from baseballReferenceScrape import getPlayersStats


#creating panda data frames for player id search and salary data search
salary_data = pd.read_csv('salary_data/salary_data.csv')



#below are the get methods for retrieving data from the data bases
#these will be called to retrive data in the easiest way possible

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
def getStatsBeforeSigning(playerName):

	getPlayersStats(playerName)

	full_name = playerName.replace(" ", "")
	player_stats = pd.read_csv('battingStatsPlayers/' + full_name.lower() + getPlayerTeam(playerName) + ".csv")

	# year_signed = getContractSignYear(playerName) - 1

	# indx = player_stats[player_stats['Year']==year_signed].index.item()
	# adjusted_player_stats = player_stats[indx]


	return player_stats

def main():


	user_input = input("Enter player who's salary you wish to see: ")
	getStatsBeforeSigning(user_input)
	print()
	print("Total Contract value:",getTotalContractValue(user_input))
	print("Salary Years:",getContractYears(user_input))
	print("Year Contract Signed:",getContractSignYear(user_input))
	print("Contract length:",getContractLength(user_input))
	print("Team:",getPlayerTeam(user_input))

main()