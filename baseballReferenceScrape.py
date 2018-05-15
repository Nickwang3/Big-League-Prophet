import bs4
import re
from urllib.request import urlopen as uReq
from urllib.request import urlretrieve
from bs4 import BeautifulSoup as soup
import csv
import requests
import pandas as pd 

#scrapes player id csv file from given website
def getPlayerIDS():

	url = 'http://crunchtimebaseball.com/baseball_map.html'

	data = requests.get('http://crunchtimebaseball.com/master.csv').text

	with open('playerIDS/IDS.csv', 'w', encoding='utf8') as file:
   		file.write(data)



#grabs players baseball reference page and downloads their stats
def getPlayersStats(brefID):
	
	try:
		my_url = "https://www.baseball-reference.com/players/" + brefID[0] + "/" + brefID + ".shtml"
	except TypeError:
		print("That player has changed teams recently or does not exist")
		return

	#downloading web page from url
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("h1", {"itemprop":"name"})
	container_player_name = containers[0].text
	print()
	print(container_player_name)
	print()
	#calls getPosition method
	print(getPosition(my_url))

	#now we need the data for the players (these will start with career statistics


	salary_table = page_soup.find('table')

	headers = [header.text for header in salary_table.findAll('th')]


	rows = []

	#grabbing the row data
	#only grabs major league stats no minor
	for trs in salary_table.find_all('tr', {'class':'full'}):
		
		th = trs.find('th').text
		tds = trs.find_all('td')
		row = [elem.text.strip() for elem in tds]
		row.insert(0, th)
		rows.append(row)

	#creating a new file naming scheme to work with other scripts 
	player_file_name = brefID + getCurrentTeam(my_url)

	#writing the csv file
	with open('baseballStatsPlayers/' + player_file_name +'.csv', 'w', encoding='utf8') as fp:
	    writer = csv.writer(fp)
	    writer.writerow(headers)
	    writer.writerows(row for row in rows if row)


#finds the players current team as initials (CURRENT PLAYERS ONLY)
def getCurrentTeam(player_page_url):

	uClient = uReq(player_page_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.find('div', {'itemtype':'https://schema.org/Person'})
	paragraph_containers = containers.findAll('p')
	player_team = paragraph_containers[3].find('a').text


	#dictionary of team names and their abbreviations
	dict_teams = {'Arizona Diamondbacks':'ARI','Atlanta Braves':'ATL','Baltimore Orioles':'BAL','Boston Red Sox':'BOS','Chicago Cubs':'CHC','Chicago White Sox':'CWS','Cincinnati Reds':'CIN',
	'Cleveland Indians':'CLE','Colorado Rockies':'COL','Detroit Tigers':'DET','Miami Marlins':'MIA','Houston Astros':'HOU','Kansas City Royals':'KC','Los Angeles Angels of Anaheim':'LAA','Los Angeles Dodgers':'LAD',
	'Milwaukee Brewers':'MIL','Minnesota Twins':'MIN','New York Mets':'NYM','New York Yankees':'NYY','Oakland Athletics':'OAK','Philadelphia Phillies':'PHI','Pittsburgh Pirates':'PIT',
	'San Diego Padres': 'SD','San Francisco Giants': 'SF','Seattle Mariners':'SEA','St. Louis Cardinals':'STL','Tampa Bay Rays': 'TB','Texas Rangers':'TEX','Toronto Blue Jays':'TOR','Washington Nationals':'WSH', 'Los Angeles Angels':'LAA'}

	team_abbrev = dict_teams[player_team]

	return team_abbrev


#finds the players position
def getPosition(player_page_url):

	uClient = uReq(player_page_url)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.find('div', {'itemtype':'https://schema.org/Person'})
	paragraph_containers = containers.findAll('p')
	player_position = paragraph_containers[0].text
	indx_replacer = player_position.find(":")
	player_position = player_position[indx_replacer+1:].strip()

	return player_position

