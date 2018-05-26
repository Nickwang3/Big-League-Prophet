from createPlayerObject import getRandomPlayer
from createPlayerObject import createPlayer
import pandas as pd
from pandas import DataFrame
import numpy

#drops the half years where a player is traded during the year, only keeps the total
def keep_only_total(name, team):

	player = createPlayer(name, team)

	key = ""
	if player.position == 'SP' or player.position == "RP":
		key = "SEASON"
	else:
		key = "YEAR"

	stats = player.stats_before_signing
	year = ''
	list_of_unwanted_indices = []

	for i in range(len(stats.index)):

		if stats['TEAM'][i] == 'Total':

			year = stats[key][i]

			for k in range(len(stats.index)):

				if stats[key][k] == year and stats['TEAM'][k] != 'Total':

					list_of_unwanted_indices.append(k)

	stats = stats.drop(stats.index[list_of_unwanted_indices])

	return stats

#not just before signing
def keep_only_total_all_stats(name, team):

	player = createPlayer(name, team)

	key = ""
	if player.position == 'SP' or player.position == "RP":
		key = "SEASON"
	else:
		key = "YEAR"

	stats = player.stats
	year = ''
	list_of_unwanted_indices = []

	for i in range(len(stats.index)):

		if stats['TEAM'][i] == 'Total':

			year = stats[key][i]

			for k in range(len(stats.index)):

				if stats[key][k] == year and stats['TEAM'][k] != 'Total':

					list_of_unwanted_indices.append(k)

	stats = stats.drop(stats.index[list_of_unwanted_indices])

	return stats

#gets the career average for a stat
def average_stat(player_stats, statistic):

	total = 0
	for i in range(len(player_stats.index)):
		total = total + player_stats[statistic][i]


	try:
		average = total / (len(player_stats.index))
	except:
		return

	average = float("{0:.2f}".format(average))
	
	return average




# takes age of players and the length of the contracts that they sign and puts them into a new data set for testing
def ageModel():

	# ageGraph = pandas.DataFrame([0,0], columns=['Age', 'Contract Length'])

	for i in range(5):
		

		player = createPlayer()
		
		# row = pandas.DataFrame([player.contract.age_at_signing, player.contract.length], columns=['Age', 'Contract Length'])

		# ageGraph.append(row)

		print(player.age_at_signing, player.contract.length)

	# return ageGraph

# ageModel()


#takes war of last year before signing and relates it average annual contract value
def warModel(iterations):

	df = DataFrame(columns=('WAR', 'Avg Annual'))

	for i in range(iterations):

		name, team = getRandomPlayer()
		player = createPlayer(name, team)

		#checks if player is arbitration eligible yet (we dont want to include players who arent)
		try:
			if player.service_time < 4:
				continue
		except:
			pass

		try:
			stats = player.stats_before_signing

			war = average_stat(stats, "WAR")

			df.loc[i] = [war, player.contract.avg_value]

		except (AttributeError, IndexError):
			pass

	return df


#determines innings, strike outs, ERA of year before signing and relates it to annual contract value
def pos_innings_Ks_ERA_model(iterations):

	df = DataFrame(columns=('POS', 'IP', 'SO', "ERA", 'Avg Annual'))

	for i in range(iterations):

		name, team = getRandomPlayer()
		player = createPlayer(name, team)

		try:
			if player.service_time < 4:
				continue
		except:
			pass

		#checks if player is a pitcher
		try:
			if player.position == 'RP' or player.position == 'SP':
		
				stats = player.stats_before_signing
				# innings = stats['IP'][stats.index[-1]]
				# strike_outs = stats['SO'][stats.index[-1]]
				# ERA = stats['ERA'][stats.index[-1]]

				innings = average_stat(stats, 'IP')
				strike_outs = average_stat(stats, 'SO')
				ERA = average_stat(stats, 'ERA')

				#need to have numbers for machine learning
				if player.position == 'SP':
					position = 1
				else:
					position = 0

				df.loc[i] = [position, innings, strike_outs, ERA, player.contract.avg_value]
			else:
				continue

		except (AttributeError, IndexError, KeyError):
			pass

	return df



#runs models and saves the train and test data
def updateWarModel():



	#update the war model
	traindfWar = warModel(600)

	traindfWar.to_csv("trainAndTestData/trainingWAR.csv", index=False, header=True)

	testdfWar = warModel(50)

	testdfWar.to_csv("trainAndTestData/testingWAR.csv", index=False, header=True)


def updatePitcherModel():

	traindfPitcher = pos_innings_Ks_ERA_model(600)

	traindfPitcher.to_csv('trainAndTestData/trainingPitcher.csv')

	testdfPitcher = pos_innings_Ks_ERA_model(50)

	testdfPitcher.to_csv('trainAndTestData/testingPitcher.csv')


def updateModels():
	
	updateWarModel()
	updatePitcherModel()




updateModels()
