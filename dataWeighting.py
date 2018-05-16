from csv_stats_reader import main as csv_main
from csv_stats_reader import createPlayerObject as createPlayer
import pandas
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


#takes war of last year before signing and relates it to total contract value
def warModel():

	for i in range(20):

		player = createPlayer()

		try:
			stats = player.stats_before_signing
			warLastSeason = stats['WAR'][stats.index[-1]]

			print (warLastSeason, player.contract.total_value, player.contract.sign_year)
		except (AttributeError, IndexError):
			print("No mlb stats available prior to signing active contract")

warModel()