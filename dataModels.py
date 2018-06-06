#here are all the machine learning models to be used for various player predictions
from dataManipulation import only_total_rows, average_stat, career_high_stat, convert_stats_to_dataframe, weight_last_3
import dataset
import pandas as pd
from pandas import DataFrame
import pandas.io.common
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


salary_data = pd.read_csv('salary_data/salary_data.csv')


#player database connection
db = dataset.connect('postgresql://baseball_project:baseball_project@localhost:5432/player_database')

table = db['players']




#war model salary predictions based on career average war before signing
def average_war_model():

	model = DataFrame(columns=('WAR', 'Avg Annual'))

	for row in salary_data.itertuples(index=True, name='Pandas'):

		try:
			team = str(getattr(row, "Team"))
			name = str(getattr(row, "Name"))
		except: 
			print("exception found")


		players = table.find(name=name)

		
		for player in players:

			try:
				actual_player = table.find_one(name=name, team=team)
			except:
				actual_player = table.find_one(name=name)

			try:
				stats = actual_player['stats_before_signing'] 
				df = convert_stats_to_dataframe(stats)

				adjusted_stats = only_total_rows(actual_player, df)

				average_war = average_stat(adjusted_stats, 'WAR')
				model.loc[len(model)] = [average_war, actual_player['average_value']]


			except (TypeError, pandas.io.common.EmptyDataError, KeyError):
				pass

	model = model.dropna()	

	model.to_csv("trainAndTestData/training_average_WAR.csv", index=False, header=True)

#weights war by recency
def recency_war_model():

	model = DataFrame(columns=('Weighted WAR', 'Avg Annual'))
	count = 0 
	for row in salary_data.itertuples(index=True, name='Pandas'):

		try:
			team = str(getattr(row, "Team"))
			name = str(getattr(row, "Name"))
		except: 
			print("exception found")


		players = table.find(name=name)

		
		for player in players:

			try:
				actual_player = table.find_one(name=name, team=team)
			except:
				actual_player = table.find_one(name=name)

			try:
				stats = actual_player['stats_before_signing'] 
				df = convert_stats_to_dataframe(stats)

				adjusted_stats = only_total_rows(actual_player, df)

				weighted_war = weight_last_3(adjusted_stats, 'WAR', int(actual_player['sign_year']))
				model.loc[len(model)] = [weighted_war, actual_player['average_value']]


			except (TypeError, pandas.io.common.EmptyDataError, KeyError):
				pass

	model = model.dropna()	

	model.to_csv("trainAndTestData/weighted_recent_WAR.csv", index=False, header=True)

def peak_war_model():

	model = DataFrame(columns=('WAR', 'Avg Annual'))

	for row in salary_data.itertuples(index=True, name='Pandas'):

		try:
			team = str(getattr(row, "Team"))
			name = str(getattr(row, "Name"))
		except: 
			print("exception found")


		players = table.find(name=name)

		
		for player in players:

			try:
				actual_player = table.find_one(name=name, team=team)
			except:
				actual_player = table.find_one(name=name)

			try:
				stats = actual_player['stats_before_signing'] 
				df = convert_stats_to_dataframe(stats)

				adjusted_stats = only_total_rows(actual_player, df)

				peak_war = career_high_stat(adjusted_stats, 'WAR')
				model.loc[len(model)] = [peak_war, actual_player['average_value']]


			except (TypeError, pandas.io.common.EmptyDataError, KeyError):
				pass

	model = model.dropna()	

	model.to_csv("trainAndTestData/training_peak_WAR.csv", index=False, header=True)


#hitters only
def triple_crown_model():

	model = DataFrame(columns=('AVG', 'HR', 'RBI', 'Avg Annual'))

	for row in salary_data.itertuples(index=True, name='Pandas'):

		try:
			team = str(getattr(row, "Team"))
			name = str(getattr(row, "Name"))
			position = str(getattr(row, "POS"))
		except: 
			print("exception found")

		if position=='SP' or position=='RP':
			continue

		players = table.find(name=name)

		
		for player in players:

			try:
				actual_player = table.find_one(name=name, team=team)
			except:
				actual_player = table.find_one(name=name)

			try:
				stats = actual_player['stats_before_signing'] 
				df = convert_stats_to_dataframe(stats)

				adjusted_stats = only_total_rows(actual_player, df)

				average_avg = int(average_stat(adjusted_stats, 'AVG'))
				average_HR = int(average_stat(adjusted_stats, 'HR'))
				average_RBI = int(average_stat(adjusted_stats, 'RBI'))


				model.loc[len(model)] = [average_avg, average_HR, average_RBI, actual_player['average_value']]


			except (TypeError, pandas.io.common.EmptyDataError, KeyError):
				pass

	model = model.dropna()	

	model.to_csv("trainAndTestData/training_triple_crown.csv", index=False, header=True)



# triple_crown_model()
recency_war_model()
# peak_war_model()
# average_war_model()
