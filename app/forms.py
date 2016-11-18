from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, InputRequired


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[InputRequired()])
