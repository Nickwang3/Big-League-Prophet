from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pandas as pd 
import dataset
from dataManipulation import only_total_rows, average_stat, career_high_stat, convert_stats_to_dataframe

db = dataset.connect('postgresql://baseball_project:baseball_project@localhost:5432/player_database')

table = db['players']

user_input = input("enter name: ")
user_input = "%" + user_input + "%"


result = db.query("SELECT * FROM players WHERE name LIKE '%s' ORDER BY average_value DESC NULLS LAST LIMIT 15" % user_input)

for row in result:
	print(row['name'], row['espn_id'], row['team'])