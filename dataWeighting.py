from csv_stats_reader import main as csv_main
from csv_stats_reader import createPlayerObject as createPlayer
from csv_stats_reader import getRandomPlayer
import pandas
from pandas import DataFrame
import numpy


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
def warModel():

	df = DataFrame(columns=('WAR', 'Avg Annual'))

	for i in range(50):

		getRandomPlayer()
		name, team = getRandomPlayer.player, getRandomPlayer.team
		player = createPlayer(name, team)

		try:
			stats = player.stats_before_signing
			warLastSeason = stats['WAR'][stats.index[-1]]

			df.loc[i] = [warLastSeason,player.contract.avg_value]

		except (AttributeError, IndexError):
			pass

	return df


