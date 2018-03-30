import bs4
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def main():
	
	print()
	#user input for finding players statistics off of Baseball Reference
	player_id = 1   #used to identify multiple players with similar url name
	players_full_name = (input("Enter player's full name: ")).lower().strip().split()
	player_first_name = players_full_name[0]
	player_last_name = players_full_name[1]
	last_name_initial = player_last_name[0]
	correct_player = False

	#still need to fix if user goes over iput limit and gets to error 404 not found
	while(correct_player==False):

		player_name = player_last_name[:5] + player_first_name[:2] + "0" + str(player_id)
		my_url = "https://www.baseball-reference.com/players/" + last_name_initial + "/" + player_name + ".shtml"

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


		#ask if given player is correct player
		user_answer = 'null'
		while user_answer != 'yes' and user_answer!= 'no':
			
			user_answer = input("Is this the correct player? Enter Yes or No: ").lower()
			print()

			if user_answer == 'yes':
				correct_player = True
			else: 
				player_id+=1


	#now we need the data for the players (these will start with career statistics)

	salary_table = page_soup.find('table')

	headers = [header.text for header in salary_table.findAll('th')]


	rows = []

	#grabbing the row data
	#only grabs major league stats no minor
	for trs in salary_table.find_all('tr', {'class':'full'}):
		
		tds = trs.find_all('td')
		row = [elem.text.strip() for elem in tds]
		rows.append(row)

	#creating a new file naming scheme to work with other scripts 
	player_file_name = player_first_name + player_last_name + getCurrentTeam(my_url)

	#writing the csv file
	with open('battingStatsPlayers/' + player_file_name +'.csv', 'w', encoding='utf8') as fp:
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
	'Cleveland Indians':'CLE','Colorado Rockies':'COL','Detroit Tigers':'DET','Florida Marlins':'FLA','Houston Astros':'HOU','Kansas City Royals':'KAN','Los Angeles Angels':'LAA','Los Angeles Dodgers':'LAD',
	'Milwaukee Brewers':'MIL','Minnesota Twins':'MIN','New York Mets':'NYM','New York Yankees':'NYY','Oakland Athletics':'OAK','Philadelphia Phillies':'PHI','Pittsburgh Pirates':'PIT',
	'San Diego Padre': 'SD','San Francisco Giant': 'SF','Seattle Mariners':'SEA','St. Louis Cardinals':'STL','Tampa Bay Ray': 'TB','Texas Rangers':'TEX','Toronto Blue Jays':'TOR','Washington Nationals':'WAS'}

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
	
main()