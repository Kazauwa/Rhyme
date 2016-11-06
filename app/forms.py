from app import db
from app.models import Album, Artist, Track
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Optional, Length


class SearchForm(FlaskForm):
    search_by_album = StringField('Album', validators=[Optional()])
    search_by_artist = StringField('Artist', validators=[Optional()])
    search_track = StringField('Track', validators=[Optional()])
    year = StringField('Year', validators=[Optional(), Length(max=4)])

    # map form fields to database fields/attributes
    __field_to_attr = {'search_by_album': Album.title,
                       'search_by_artist': Artist.name,
                       'search_track': Track.title,
                       'year': Album.year}

    def construct_query(self):
        query = db.session.query(*[field.label.text for field in self if field.data and not field.name == 'csrf_token'])
        for field in self:
            if field.data and not field.name == 'csrf_token':
                query = query.filter(self.__field_to_attr[field.name] == field.data)
        result = query.all()
        return result

    def validate(self):
        #FIXME
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
