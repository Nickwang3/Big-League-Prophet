# first grab a player's id and find that players statistics, position, and team from crunchtime baseball
# then assign each player on the salary chart their ID
# use ID to search for players contract information to create the contract object
# create the player object with the contract included
# create the player object database which will allow for faster player data retrieval
# take a players statistics and create their salary predictions
# create the Predictions database which has a player's id and their corresponding predictions
import dataset
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pandas as pd 
from playerAndContract import Player, Contract
from getPlayerStats import getPlayerStats, getServiceTime

#using dataset for easy use of postgres with python
db = dataset.connect('postgresql://baseball_project:baseball_project@localhost:5432/player_database')

table = db['players']


salary_data = pd.read_csv('salary_data/salary_data.csv')

player_IDS = pd.read_csv('playerIDS/IDS.csv', encoding='ANSI')

count = 0
for row in player_IDS.itertuples(index=True, name='Pandas'):

	try:
		#grabbing player information from ID file
		mlb_name = str(getattr(row, "mlb_name"))
		espn_name = str(getattr(row, "espn_name"))
		cbs_name = str(getattr(row, "cbs_name"))
		position = str(getattr(row, "mlb_pos"))
		team = str(getattr(row, "mlb_team"))
		espn_id = str(int(getattr(row, "espn_id")))
		birth_year = int(getattr(row, "birth_year"))
		bats = str(getattr(row, "bats"))
		throws = str(getattr(row, "throws"))

	except:
		pass
	
	contract_df = []
		#check if player is in salary data base (could be under a few possible names)
	if mlb_name in salary_data.Name.values:
		contract_df = salary_data[salary_data.Name==mlb_name]
	elif espn_name in salary_data.Name.values:
		contract_df = salary_data[salary_data.Name==espn_name]
	elif cbs_name in salary_data.Name.values:
		contract_df = salary_data[salary_data.Name==cbs_name]
	else:
		contract_df = None #no contract is found for player 

	#checking if there are players with the same name
	try:	
		if len(contract_df.index) > 1:
			for row in contract_df.itertuples(index=True, name='Pandas'):

				if contract_df[contract_df.POS!=position]:
					contract_df.drop(row)
				elif contract_df[contract_df.Team!=team]:
					contract_df.drop(row)
	except:
		pass

	#now that we have found the player in the salary data, get player's contract data
	try:
		for row in contract_df.itertuples(index=True, name='Pandas'):
			sign_year = int(getattr(row, "Years_Signed"))
			years_active = getattr(row, "Years_Active")
			length = int(getattr(row, "Contract_Length"))
			total_value = int(getattr(row, "int_value"))
			avg_value = int(getattr(row, "int_annual"))
			current_salary = int(getattr(row, "int_salary"))	
	except:
		sign_year = None
		years_active = None
		length = None
		total_value = None
		avg_value = None
		current_salary = None

	print(mlb_name)
	#now grab the stats for the player
	try:
		player_stats = getPlayerStats(espn_id, espn_name)
		player_stats = player_stats.reindex(axis=0)
	except:
		player_stats = None
	
	# print(list(player_stats.columns.values))


	#grabbing stats from before their active contract
	if sign_year != None:
		try:
			if position == 'P':
				stats_before_signing = player_stats[player_stats.SEASON.astype(int) < sign_year]
			else:
				stats_before_signing = player_stats[player_stats.YEAR.astype(int) < sign_year]
		except:
			stats_before_signing = None
	else:
		stats_before_signing = None

	try:
		age_at_signing = sign_year - birth_year
	except TypeError:
		age_at_signing = None

	try:
		player_stats = player_stats.to_csv()
		stats_before_signing = stats_before_signing.to_csv()
	except AttributeError:
		pass

	service_time = getServiceTime('http://www.espn.com/mlb/player/stats/_/id/' + espn_id + "/" + espn_name)


	#entering the data into the database
	table.upsert(dict(espn_id=espn_id, name=espn_name, team=team, stats=player_stats, stats_before_signing=stats_before_signing, position=position, age_at_signing=age_at_signing, service_time=service_time, length=length, years=years_active, total_value=total_value, current_salary=current_salary, average_value=avg_value, sign_year=sign_year), ['espn_id'])
	



	


