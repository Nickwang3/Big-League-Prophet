from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField

class SearchNameForm(FlaskForm):
   player_name = TextField("Name Of Player")
   team = TextField("Team abbreviation (All Caps)")
   submit = SubmitField("Search")

