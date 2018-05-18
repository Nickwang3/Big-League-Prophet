import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import locale
locale.setlocale(locale.LC_ALL, "en_US")



def predictSalaryWarModel():

	trainData = pd.read_csv("trainAndTestData/trainingWAR.csv")
	testData = pd.read_csv("trainAndTestData/testingWAR.csv")

	regr = linear_model.LinearRegression()

	x_train = trainData['WAR'].values
	y_train = trainData['Avg Annual'].values

	x_train = x_train.reshape(x_train.size, 1)
	y_train = y_train.reshape(y_train.size, 1)

	regr.fit(x_train, y_train)

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
	plt.scatter(x_train, y_train,  color='black')
	plt.plot(x_train, regr.predict(x_train), color='blue', linewidth=3)
	plt.xticks(())
	plt.yticks(())
	plt.show()



def testWarModels():

	trainData = pd.read_csv("trainAndTestData/trainingWAR.csv")
	testData = pd.read_csv("trainAndTestData/testingWAR.csv")

	regr = linear_model.LinearRegression()

	x_train = trainData['WAR'].values
	y_train = trainData['Avg Annual'].values

	x_train = x_train.reshape(x_train.size, 1)
	y_train = y_train.reshape(y_train.size, 1)

	x_test = testData['WAR'].values
	y_test = testData['Avg Annual'].values

	x_test = x_test.reshape(x_test.size, 1)
	y_test = y_test.reshape(y_test.size, 1)

	regr.fit(x_train, y_train)


	prediction = (regr.predict(x_test))

	# The coefficients
	print('Coefficients: \n', regr.coef_)
	# The mean squared error
	print("Mean squared error: %.2f" % mean_squared_error(y_test, prediction))
	# Explained variance score: 1 is perfect prediction
	print('Variance score: %.2f' % r2_score(y_test, prediction))


	#shows the best fit line in a graph
	plt.scatter(x_test, y_test,  color='black')
	plt.plot(x_test, prediction, color='blue', linewidth=3)
	plt.xticks(())
	plt.yticks(())
	plt.show()

def predictSalaryPitcherModel():

	trainData = pd.read_csv("trainAndTestData/trainingPitcher.csv")
	testData = pd.read_csv("trainAndTestData/testingPitcher.csv")

	regr = linear_model.Lasso(alpha = 0.01)

	x_train = trainData[['IP', 'SO', 'ERA']]
	x_train = x_train.values.reshape(-1,3)
	y_train = trainData['Avg Annual'].values

	x_test = testData[['IP', 'SO', 'ERA']]
	x_test = x_test.values.reshape(-1,3)
	y_test = testData['Avg Annual'].values


	regr.fit(x_train, y_train)

	predictions = (regr.predict(x_test))

	user_input_ip, user_input_so, user_input_era = input("Enter players IP, SO, and ERA (seperated by a space): \n").split()
	ip = float(user_input_ip)
	so = float(user_input_so)
	era = float(user_input_era)

	test_var = [[ip, so, era]]

	prediction = regr.predict(test_var)
	prediction = int(prediction[0])

	formatted_prediction = locale.format("%d", prediction, grouping=True)
	formatted_prediction = "$"+formatted_prediction
	
	print()
	print("The predicted annual salary for a player with those statistics is", formatted_prediction)



predictSalaryPitcherModel()
predictSalaryWarModel()