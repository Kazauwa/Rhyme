from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, Length


class SearchForm(FlaskForm):
    search_by_album = StringField('Album', validators=[Optional()])
    search_by_artist = StringField('Artist', validators=[Optional()])
    search_track = StringField('Track', validators=[Optional()])
    year = StringField('Year', validators=[Optional(), Length(max=4)])

    def validate(self):
        if not super().validate():
            return False
        if not self.search_by_album and not self.search_by_artist and not self.search_track and not self.year:
            msg = 'At least one of the search fields must be set!'
            self.search_by_album.errors.append(msg)
            self.search_by_artist.errors.append(msg)
            self.search_track.errors.append(msg)
            self.year.errors.append(msg)
            return False
        return True
