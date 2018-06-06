from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pandas as pd 
import dataset
from dataManipulation import only_total_rows, average_stat, career_high_stat, convert_stats_to_dataframe

db = dataset.connect('postgresql://baseball_project:baseball_project@localhost:5432/player_database')

table = db['players']

result = db.query('SELECT * FROM players ORDER BY average_war_salary_prediction DESC NULLS LAST LIMIT 20')

for row in result:
	print(row['name'], row['average_war_salary_prediction'])