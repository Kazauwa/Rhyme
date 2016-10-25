from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional


class SearchForm(FlaskForm):
    search_by_album = StringField('search_by_album', validators=[Optional()])
    search_by_artist = StringField('search_by_artist', validators=[Optional()])
    search_track = StringField('search_track', validators=[Optional()])
    year = IntegerField('year', validators=[Optional()])

    def validate(self):
        if not super().validate():
            return False
        if not self.search_by_album and not self.search_by_artist and not self.search_track:
            msg = 'At least one of the search fields must be set!'
            self.search_by_album.errors.append(msg)
            self.search_by_artist.errors.append(msg)
            self.search_track.errors.append(msg)
            return False
        return True
