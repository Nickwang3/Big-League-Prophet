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

def getPlayerStats(espnID, espn_name):
	
	espnName = espn_name.replace(" ","-")

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
	df 


	#doesnt drop last column if player has just one year of stats
	if len(df.index) > 2:
		df = df.drop(df.index[-1])
		df = df.drop(df.index[-1])


	df = df.rename(columns=df.iloc[0])
	df = df.drop(df.index[0])
	df = df.reset_index()
	df.columns = df.columns.to_series().apply(lambda x: x.strip())
	del df['index']

	career_statistics = df

	player_file_name = espnName.replace(" ", "-") + "#" + espnID

	#writing the csv file
	return career_statistics

def getServiceTime(player_page_url):

		page_html = requests.get(player_page_url).text

		page_soup = soup(page_html, "html.parser")

		container = page_soup.find('ul', {"class":"player-metadata floatleft"})

		try:
			li = container.find_all('li')
		except:
			return None

		try:
			time = li[2].text
			time = time.split()
			time = time[0]
			time = time[10:]
			return(int(time))
		except:
			return None

# print(getPlayerStats('31050', "aj jimenez"))
# print(getPlayerStats('33039', "mookie betts"))