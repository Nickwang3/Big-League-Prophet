# machineLearningBaseball


run salaryDataReader.py to update salary data file

mlbScraper.py is called upon by createPlayerObject.py to grab a players statistics from ESPN

run PlayerDatabase.py to update the postgreSQL player database

run dataWeighting.py to update prediction models

to run the program, run flaskbootstrapapp.py 

currently the website allows user to enter a player and the team they are on and it will display their stats and a prediction for annual salary based on average war and 
peak war for their career


SOURCES FOR DATA:

	
USA TODAY for Salary data

ESPN for player statistics

http://crunchtimebaseball.com/baseball_map.html for playerIDS