import bs4
import re
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as soup
import csv
import requests
import pandas as pd 
import lxml
import html5lib




#scrapes player id csv file from given website
def getPlayerIDS():

	url = 'http://crunchtimebaseball.com/baseball_map.html'

	data = requests.get('http://crunchtimebaseball.com/master.csv').text

	with open('playerIDS/IDS.csv', 'w', encoding='utf8') as file:
   		file.write(data)

#birth year of player
def getBirthYear(player_page_url):

	page_html = requests.get(player_page_url).text

	page_soup = soup(page_html, "html.parser")

	container = page_soup.find('ul', {"class":"player-metadata floatleft"})
	try:
		year = container.find('li').text
		year = year.split()
	except:
		return -1

	return int(year[3])

def getServiceTime(player_page_url):

		page_html = requests.get(player_page_url).text

		page_soup = soup(page_html, "html.parser")

		container = page_soup.find('ul', {"class":"player-metadata floatleft"})

		try:
			li = container.find_all('li')
		except:
			return -1

		try:
			time = li[2].text
			time = time.split()
			time = time[0]
			time = time[10:]
			return(int(time))
		except:
			return -1



#finds the players position
def getPosition(player_page_url):


	page_html = requests.get(player_page_url).text

	page_soup = soup(page_html, "html.parser")

	position = page_soup.find('li', {"class":"first"}).text

	player_position = position.split()

	return player_position[1]

#finds the players current team as initials (CURRENT PLAYERS ONLY)
def getCurrentTeam(player_page_url):


	page_html = requests.get(player_page_url).text

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.find('li', {'class':'last'})
	player_team = containers.text


	#dictionary of team names and their abbreviations
	dict_teams = {'Arizona Diamondbacks':'ARI','Atlanta Braves':'ATL','Baltimore Orioles':'BAL','Boston Red Sox':'BOS','Chicago Cubs':'CHC','Chicago White Sox':'CWS','Cincinnati Reds':'CIN',
	'Cleveland Indians':'CLE','Colorado Rockies':'COL','Detroit Tigers':'DET','Miami Marlins':'MIA','Houston Astros':'HOU','Kansas City Royals':'KC','Los Angeles Angels of Anaheim':'LAA','Los Angeles Dodgers':'LAD',
	'Milwaukee Brewers':'MIL','Minnesota Twins':'MIN','New York Mets':'NYM','New York Yankees':'NYY','Oakland Athletics':'OAK','Philadelphia Phillies':'PHI','Pittsburgh Pirates':'PIT',
	'San Diego Padres': 'SD','San Francisco Giants': 'SF','Seattle Mariners':'SEA','St. Louis Cardinals':'STL','Tampa Bay Rays': 'TB','Texas Rangers':'TEX','Toronto Blue Jays':'TOR','Washington Nationals':'WSH', 'Los Angeles Angels':'LAA'}

	try:
		team_abbrev = dict_teams[player_team]
	except KeyError:
		team_abbrev = "FreeAgent"


	return team_abbrev


#grabs players baseball reference page and downloads their stats
def getPlayersStats(espnID, playerName):
	
	espnName = playerName.replace(" ","-")

	try:
		my_url = 'http://www.espn.com/mlb/player/stats/_/id/' + espnID + "/" + espnName
	except (KeyError, TypeError):
		return


	page_html = requests.get(my_url).text

	#html parsing
	page_soup = soup(page_html, "html.parser")

	name = page_soup.find('h1').text

	#using pandas to read the career statistics
	try:
		dfs = pd.read_html(my_url)
	except ValueError:
		return -1
	df = dfs[1]


	df = df.drop(df.index[0]) 


	#doesnt drop last column if player has just one year of stats
	if len(df.index) > 2:
		df = df.drop(df.index[-1])
		df = df.drop(df.index[-1])

	career_statistics = df

	player_file_name = espnName.replace(" ", "-") + "#" + espnID

	#writing the csv file
	career_statistics.to_csv("baseballStatsPlayers/"+player_file_name+".csv", index=False, header=False)


#grabs a list of all players who signed an extension or signed as a free agent
def getFreeAgentList():

	url = "https://www.mlbtraderumors.com/extensiontracker.html"

	

