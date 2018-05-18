import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dataWeighting import warModel
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
import locale
locale.setlocale(locale.LC_ALL, "en_US")



def main():

	trainData = pd.read_csv("trainAndTestData/trainingWAR.csv")
	# trainData = warModel()
	# trainData.to_csv("trainAndTestData/trainingWAR.csv", index=False, header=True)

	regr = linear_model.LinearRegression()

	x = trainData['WAR'].values
	y = trainData['Avg Annual'].values

	x = x.reshape(x.size, 1)
	y = y.reshape(y.size, 1)

	regr.fit(x, y)

	#ask for user input on a player
	# player_name = input("Enter a player who's predicted salary you would like to see (prediction is based on season's WAR): ")
	# season = input("Enter player's most recent fully completed season: ")

	print()
	user_input = float(input("Enter player's WAR: "))

	prediction = int(regr.predict(user_input))

	formatted_prediction = locale.format("%d", prediction, grouping=True)
	formatted_prediction = "$"+formatted_prediction
	
	print()
	print("The predicted annual salary for a player of WAR",user_input, "is", formatted_prediction)


	#shows the best fit line in a graph
	plt.scatter(x, y,  color='black')
	plt.plot(x, regr.predict(x), color='blue', linewidth=3)
	plt.xticks(())
	plt.yticks(())
	plt.show()

main()
