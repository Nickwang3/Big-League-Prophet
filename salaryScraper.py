import csv
import bs4
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def getSalaryData():


	my_url = "https://www.usatoday.com/sports/mlb/salaries/"

	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	salary_table = page_soup.find('table')

	headers = [header.text for header in salary_table.findAll('th')]


	rows = []

	#grabbing the row data
	for trs in salary_table.find_all('tr'):
		tds = trs.find_all('td')
		row = [elem.text.strip() for elem in tds]
		rows.append(row)

	#writing the csv file
	with open('salary_data/salary_data.csv', 'w', encoding='utf8') as fp:
	    writer = csv.writer(fp)
	    writer.writerow(headers)
	    writer.writerows(row for row in rows if row)

