from app import db


tracklist = db.Table('tracklist',
                     db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
                     db.Column('track_id', db.Integer, db.ForeignKey('track.id')))

releases = db.Table('releases',
                    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
                    db.Column('track_id', db.Integer, db.ForeignKey('track.id')))

style = db.Table('style',
                 db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
                 db.Column('album_id', db.Integer, db.ForeignKey('album.id')))


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.String(4))
    cover = db.Column(db.String(128), unique=True)
    thumb = db.Column(db.String(128), unique=True)
    discogs_id = db.Column(db.Integer)
    tracklist = db.relationship('Track', secondary=tracklist,
                                backref=db.backref('albums', lazy='dynamic'),
                                lazy='dynamic')
    genre = db.relationship('Genre', secondary=style,
                            backref=db.backref('albums', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return '<Album %r>' % self.title


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    duration = db.Column(db.String(6))
    position = db.Column(db.Integer)

    def __repr__(self):
        return '<Track %r>' % self.title


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    image = db.Column(db.String(128))
    thumb = db.Column(db.String(128))
    discogs_id = db.Column(db.Integer)
    releases = db.relationship('Track', secondary=releases,
                               backref=db.backref('artists', lazy='dynamic'),
                               lazy='dynamic')

    def __repr__(self):
        return '<Artist %r>' % self.name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return '<Genre %r>' % self.genre
