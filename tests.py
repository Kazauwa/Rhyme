#!flask/bin/python

import unittest
import os
from app import app, db
from app.models import Album, Artist, Track
from coverage import coverage
from config import BASEDIR
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TESTDB_URI')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def test_search(self):
        album = Album(title='test_album', year='9999')
        artist = Artist(name='test_artist')
        track_1 = Track(title='test_track_1', position=1)
        track_2 = Track(title='test_track_2', position=2)
        artist.releases.append(album)
        album.tracklist.append(track_1)
        album.tracklist.append(track_2)
        db.session.add(track_1)
        db.session.add(track_2)
        db.session.add(album)
        db.session.add(artist)
        db.session.commit()
        query = Artist.query.first()
        assert query.name == 'test_artist'
        query = query.releases.first()
        assert query.title == 'test_album'
        assert query.year == '9999'
        query = query.tracklist.all()
        assert query[0].title == 'test_track_1'
        assert query[0].position == '1'
        assert query[1].title == 'test_track_2'
        assert query[1].position == '2'


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass  # passes the exceptions in order to complete the report
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(BASEDIR, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
