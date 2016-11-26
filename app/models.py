import re
from app import db

style = db.Table('style',
                 db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
                 db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))

collection = db.Table('collection',
                      db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return '{0}'.format(self.genre)


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
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
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
    releases = db.relationship('Album', backref='artist', lazy='dynamic')

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
        results = cls.query.filter(cls.search_text.ilike('%{0}%'.format(query))).all()
        yield Artist.query.filter(Artist.id.in_(
            [result.object_id for result in results if result.model_type == 'artist'])).limit(5).all()
        yield Album.query.filter(Album.id.in_([
            result.object_id for result in results if result.model_type == 'album'])).limit(5).all()
        yield Track.query.filter(Track.id.in_(
            [result.object_id for result in results if result.model_type == 'track'])).limit(5).all()

    @classmethod
    def search_artist(cls, query):
        results = cls.query.filter(
            cls.search_text.ilike('%{0}%'.format(query))).filter(cls.model_type == 'artist').all()
        objectives = [result.object_id for result in results]
        return Artist.query.filter(Artist.id.in_(objectives)).all()

    @classmethod
    def search_album(cls, query):
        results = cls.query.filter(
            cls.search_text.ilike('%{0}%'.format(query))).filter(cls.model_type == 'album').all()
        objectives = [result.object_id for result in results]
        return Album.query.filter(Album.id.in_(objectives)).all()

    @classmethod
    def search_track(cls, query):
        results = cls.query.filter(
            cls.search_text.ilike('%{0}%'.format(query))).filter(cls.model_type == 'track').all()
        objectives = [result.object_id for result in results]
        return Track.query.filter(Track.id.in_(objectives)).all()

    def __repr__(self):
        return '<{0}: {1}, id: {2}>'.format(self.model_type,
                                            self.search_text,
                                            self.object_id)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    nickname = db.Column(db.String(32), unique=True)
    profile_pic = db.Column(db.String(256), unique=True)
    thumb = db.Column(db.String(256), unique=True)
    vk_id = db.Column(db.Integer, unique=True)
    sex = db.Column(db.Integer())
    collection = db.relationship('Album', secondary=collection,
                                 primaryjoin=(collection.c.user_id == id),
                                 secondaryjoin=(collection.c.album_id == Album.id),
                                 backref=db.backref('user\'s collection', lazy='dynamic'),
                                 lazy='dynamic')

    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

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

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def add_album(self, album):
        if not self.has_album(album):
            self.collection.append(album)
            return self

    def remove_album(self, album):
        if self.has_album(album):
            self.collection.remove(album)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def has_album(self, album):
        return self.collection.filter(collection.c.album_id == album.id).count() > 0

    def latest(self):
        return self.collection.all()[:-7:-1]

    def __repr__(self):
        return '<User {0}>'.format(self.nickname)
