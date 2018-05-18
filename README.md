# machineLearningBaseball


run salaryDataReader.py to update salary data file

createPlayerObject.py retrieves data for a given player and creates a player object that
has attributes like contract data and mlb statistics

mlbScraper.py is called upon by createPlayerObject.py to grab a players statistics from ESPN

run updatePlayerStats.py to update all statistics (takes approximately 15 minutes)

to run the program, run salaryPredictor.py

the program will ask you to enter a player's WAR (wins above replacement) from a full season and it will
predict an annual salary value for that player



SOURCES FOR DATA:

	
USA TODAY for Salary data

ESPN for player statistics

http://crunchtimebaseball.com/baseball_map.html for playerIDS