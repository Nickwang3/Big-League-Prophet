#manipulation of stats for players 
import pandas as pd
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO


#gets rid of rows where of same year only keeps total stats
def only_total_rows(player, stats):

	if player['position'] == 'P':
		key = "SEASON"
	else:
		key = "YEAR"

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
	# for i in range(len(player_stats.index)):
	# 	total = total + player_stats[statistic][i]
	total = player_stats[statistic].sum()

	try:
		average = total / (len(player_stats.index))
	except:
		return

	average = float("{0:.2f}".format(average))
	
	return average


def career_high_stat(player_stats, statistic):

	career_high = 0

	# for i in range(len(player_stats.index)):
	# 	if player_stats[statistic][i] > career_high:
	# 		career_high = player_stats[statistic][i]

	try:
		career_high = player_stats[statistic].max()
	except:
		career_high = None

	# if career_high == -10:
	# 	return None

	return career_high


def convert_stats_to_dataframe(stats):

	stats = StringIO(stats)
	df = pd.read_table(stats, sep=",")

	return df