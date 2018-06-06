import dataset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pandas import DataFrame
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from dataManipulation import average_stat, only_total_rows, convert_stats_to_dataframe, career_high_stat, weight_last_3
import pandas.io.common
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO



db = dataset.connect('postgresql://baseball_project:baseball_project@localhost:5432/player_database')

table = db['players']

player_IDS = pd.read_csv('playerIDS/IDS.csv', encoding='ANSI')

espn_id_list = []

for espn_id in player_IDS.espn_id.values:
	try:
		espn_id_list.append(str(int(espn_id)))
	except ValueError:
		pass


def add_average_war_predictions():

	trainData = pd.read_csv("trainAndTestData/training_average_WAR.csv")

	regr = linear_model.LinearRegression()

	x_train = trainData['WAR'].values
	y_train = trainData['Avg Annual'].values

	x_train = x_train.reshape(x_train.size, 1)
	y_train = y_train.reshape(y_train.size, 1)

	regr.fit(x_train, y_train)

	#create all player predictions
	for espn_id in espn_id_list:

		player = table.find_one(espn_id=espn_id)

		try:
			stats = player['stats'] 
			stats = convert_stats_to_dataframe(stats)
			stats = only_total_rows(player, stats)
			average_war = average_stat(stats, 'WAR')

			prediction = int(regr.predict(average_war))

			if prediction < 545000:
				prediction = 545000
			print(prediction)

		except (pandas.io.common.EmptyDataError, ValueError, KeyError):
			prediction=None

		#insert predictions into player database
		table.upsert(dict(espn_id=espn_id, average_war_salary_prediction=prediction), ['espn_id'])


def add_peak_war_predictions():

	trainData = pd.read_csv("trainAndTestData/training_peak_WAR.csv")

	regr = linear_model.LinearRegression()

	x_train = trainData['WAR'].values
	y_train = trainData['Avg Annual'].values

	x_train = x_train.reshape(x_train.size, 1)
	y_train = y_train.reshape(y_train.size, 1)

	regr.fit(x_train, y_train)

	#create all player predictions
	for espn_id in espn_id_list:

		player = table.find_one(espn_id=espn_id)

		try:
			stats = player['stats'] 
			stats = convert_stats_to_dataframe(stats)
			stats = only_total_rows(player, stats)
			peak_war = career_high_stat(stats, 'WAR')

			prediction = int(regr.predict(peak_war))

			if prediction < 545000:
				prediction = 545000
			print(prediction)

		except (pandas.io.common.EmptyDataError, ValueError, KeyError):
			prediction=None

		#insert predictions into player database
		table.upsert(dict(espn_id=espn_id, peak_war_salary_prediction=prediction), ['espn_id'])


def add_triple_crown_salary_predictions():

	trainData = pd.read_csv("trainAndTestData/training_triple_crown.csv")

	regr = linear_model.Lasso(alpha = 0.01)

	x_train = trainData[['AVG', 'HR', 'RBI']].values
	y_train = trainData['Avg Annual'].values

	# y_train = y_train.reshape(y_train.size, 1)

	regr.fit(x_train, y_train)

	#create all player predictions
	for espn_id in espn_id_list:

		player = table.find_one(espn_id=espn_id)

		try:
			if player['position'] != 'P':
				stats = player['stats'] 
				stats = convert_stats_to_dataframe(stats)
				stats = only_total_rows(player, stats)

				average_avg = average_stat(stats, 'AVG')
				average_HR = average_stat(stats, 'HR')
				average_RBI = average_stat(stats, 'RBI')

				prediction = int(regr.predict([[average_avg, average_HR, average_RBI]]))

				prediction = int(prediction)

				if prediction < 545000:
					prediction = 545000
				print(prediction)
			else:
				prediction = None
		except (pandas.io.common.EmptyDataError, KeyError):
			prediction = None

		#insert predictions into player database
		table.upsert(dict(espn_id=espn_id, triple_crown_salary_prediction=prediction), ['espn_id'])


def add_weighted_war_predictions():

	trainData = pd.read_csv("trainAndTestData/weighted_recent_WAR.csv")

	regr = linear_model.LinearRegression()

	x_train = trainData['Weighted WAR'].values
	y_train = trainData['Avg Annual'].values

	x_train = x_train.reshape(x_train.size, 1)
	y_train = y_train.reshape(y_train.size, 1)

	regr.fit(x_train, y_train)

	#create all player predictions
	for espn_id in espn_id_list:

		player = table.find_one(espn_id=espn_id)

		try:
			stats = player['stats'] 
			stats = convert_stats_to_dataframe(stats)
			stats = only_total_rows(player, stats)
			weighted_war = weight_last_3(stats, 'WAR', 2017) #last completed mlb season

			prediction = int(regr.predict(weighted_war))

			if prediction < 545000:
				prediction = 545000
			print(prediction)

		except (pandas.io.common.EmptyDataError, ValueError, KeyError):
			prediction=None

		#insert predictions into player database
		table.upsert(dict(espn_id=espn_id, weighted_war_salary_prediction=prediction), ['espn_id'])


# add_triple_crown_salary_predictions()
# add_peak_war_predictions()
# add_average_war_predictions()
add_weighted_war_predictions()
