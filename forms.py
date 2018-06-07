from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField

class SearchNameTeamForm(FlaskForm):
   player_name = TextField("Name Of Player")
   team = TextField("Team abbreviation (All Caps)")
   submit = SubmitField("Search")

class SearchNameForm(FlaskForm):
   player_name = TextField("Name Of Player")
   submit = SubmitField("Search")