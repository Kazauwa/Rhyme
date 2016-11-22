from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, InputRequired


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[InputRequired()])


class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if not self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append('This nickname gas invalid characters. Use letters, '
                                        'numbers, undersocre and dots only.')
            return False
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in use. Please '
                                        'choose another one.')
