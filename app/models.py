from app import db

releases = db.Table('releases',
                    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
                    db.Column('album_id', db.Integer, db.ForeignKey('album.id')))

style = db.Table('style',
                 db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
                 db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return '<Genre %r>' % self.genre


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    duration = db.Column(db.String())
    position = db.Column(db.String())
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

    def get_search_term(self):
        return '{0}'.format(self.title)

    def __repr__(self):
        return '<Track {0}>'.format(self.title)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    year = db.Column(db.String(4))
    cover = db.Column(db.String(512), unique=True)
    thumb = db.Column(db.String(512), unique=True)
    discogs_id = db.Column(db.Integer, unique=True)
    tracklist = db.relationship('Track', backref='album', lazy='dynamic')
    genre = db.relationship('Genre', secondary=style,
                            primaryjoin=(style.c.album_id == id),
                            secondaryjoin=(style.c.genre_id == Genre.id),
                            backref=db.backref('albums', lazy='dynamic'),
                            lazy='dynamic')

    def get_search_term(self):
        return '{0} {1}'.format(self.title, self.year)

    def __repr__(self):
        return '<Album {0}>'.format(self.title)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    image = db.Column(db.String(512))
    thumb = db.Column(db.String(512))
    discogs_id = db.Column(db.Integer, unique=True)
    releases = db.relationship('Album', secondary=releases,
                               primaryjoin=(releases.c.artist_id == id),
                               secondaryjoin=(releases.c.album_id == Album.id),
                               backref=db.backref('artists', lazy='dynamic'),
                               lazy='dynamic')

    def get_search_term(self):
        return '{0}'.format(self.name)

    def __repr__(self):
        return '<Artist {0}>'.format(self.name)


class SearchIndex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_text = db.Column(db.String(256))
    model_type = db.Column(db.String(64))
    object_id = db.Column(db.Integer)

    @classmethod
    def search_all(cls, query):
        return cls.query.filter(cls.search_text.ilike('%{0}%'.format(query))).all()

    @classmethod
    def search_artist(self, query):
        results = self.query.filter(
            self.search_text.ilike('%{0}%'.format(query))).filter(self.model_type == 'artist').all()
        objectives = [result.object_id for result in results]
        return Artist.query.filter(Artist.id.in_(objectives)).all()

    @classmethod
    def search_album(self, query):
        results = self.query.filter(
            self.search_text.ilike('%{0}%'.format(query))).filter(self.model_type == 'album').all()
        objectives = [result.object_id for result in results]
        return Album.query.filter(Album.id.in_(objectives)).all()

    @classmethod
    def search_track(self, query):
        results = self.query.filter(
            self.search_text.ilike('%{0}%'.format(query))).filter(self.model_type == 'track').all()
        objectives = [result.object_id for result in results]
        return Track.query.filter(Track.id.in_(objectives)).all()

    def __repr__(self):
        return '<{0}: {1}, id: {2}>'.format(self.model_type,
                                            self.search_text,
                                            self.object_id)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    vk_id = db.Column(db.Integer, unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.nickname)
