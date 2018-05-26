from flask import Flask, render_template, request, redirect, flash
from flask_bootstrap import Bootstrap 
import pandas as pd 
from createPlayerObject import createPlayer
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from wtforms import Form, StringField
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from forms import SearchNameForm
import locale


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'development key'


@app.route('/')
def index():
	return render_template("index.html")


@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/prediction-models')
def models():
	return render_template("prediction_models.html")

#searches for players
@app.route('/players', methods=['GET', 'POST'])
def players():
	form = SearchNameForm()

	try:
		if form.validate_on_submit():
			name = form.player_name.data
			team = form.team.data 
			name = name.split()
			first = name[0]
			last = name[1]
			return redirect('/players/' + team + "/" + first + "-" + last)
	except AttributeError:
		return redirect('/players')

	return render_template("players.html", form=form)

#specific player page where all kinds of stats and predictions can be found
@app.route("/players/<team>/<first>-<last>")
def return_player(first, last, team):
	name = first + " " + last
	player = createPlayer(name, team)

	espn_id = player.espn_id

	war_salary_df = pd.read_csv("SalaryPredictions/WarModel.csv")

	salary = war_salary_df.loc[war_salary_df['Espn_id'] == int(espn_id)]['War_salary_prediction'].values

	salary = int(salary)

	formatted_salary = '{0:,d}'.format(salary)
	formatted_salary = "$"+formatted_salary

	return render_template("playerpage.html", player=player, title=player.name, salary=salary, formatted_salary=formatted_salary)


#the navigation bar at top of page
nav = Nav()

@nav.navigation()
def mynavbar():
    return Navbar(
        'Big League Prophet',
        View('Home', 'index'),
        View('Players', 'players'),
        View('Prediction Models', 'models'),
        View('About', 'about'),
    )


nav.init_app(app)

if __name__ == '__main__':
	app.run(debug=True)