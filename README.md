# machineLearningBaseball

scraper files are individualy run to scrape salary data and players statistics. 
These programs save files in the corresponding directories.

csv_stats_reader file contains methods for framing and retrieving data from these csv files 

when running the csv_stats_reader file there are two options, a random script of players or user input which you may change in the main function of csv_stats_reader.py 

for user input, enter a players full name and Team abreviation in all caps that you wish to search for. Players must be active MLB players with signed contracts
it will return current contract data for the player and their statistics and download a csv file for the players stats, as well as updating scraped databases

if using the script, it will give a random sample of 20 active major league players