from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_by_album = StringField('search_by_album', validators=[DataRequired()])
    save_to_json = BooleanField('save_to_json', default=False)
