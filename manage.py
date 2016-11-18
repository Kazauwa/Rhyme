#!flask/bin/python
import sys
import requests
import xml.etree.ElementTree as etree
from app import manager, db
from app.models import Genre, Album, Artist, Track, SearchIndex
from config import HEADERS, DISCOGS_MASTER
from flask_migrate import MigrateCommand
from tqdm import tqdm


@manager.command
def fill_db(dump):
    '''Fill db using discogs dump. Requires dump name as a parameter'''
    print('Processing dump. Please wait...')
    tree = etree.parse(dump)
    root = tree.getroot()
    print('Filling database:')
    for child in tqdm(root):
        genres = [genre.text for genre in child.findall('genres/genre')]
        styles = [style.text for style in child.findall('styles/style')]
        genres += styles
        album_title = child.find('title').text
        album_id = child.attrib.get('id')
        year = child.find('year').text
        artist_id = child.find('artists/artist/id').text
        album = Album(title=album_title,
                      discogs_id=album_id,
                      year=year)
        try:
            for genre in genres:
                if not Genre.query.filter(Genre.genre == genre).first():
                    db.session.add(Genre(genre=genre))
                    db.session.commit()
                genre = Genre.query.filter(Genre.genre == genre).first()
                album.genre.append(genre)
            if not Artist.query.filter(Artist.discogs_id == artist_id).first():
                artist = Artist(name=child.find('artists/artist/name').text,
                                discogs_id=artist_id)
                db.session.add(artist)
                db.session.commit()
            artist = Artist.query.filter(Artist.discogs_id == artist_id).first()
            artist.releases.append(album)
            db.session.add(album)
            db.session.add(artist)
            db.session.commit()
        except:
            # TODO: remove later
            print(sys.exc_info())
            db.session.rollback()


@manager.command
def fill_track():
    '''Fill Track entity'''
    for album in tqdm(Album.query.filter(Album.tracklist == None).all()):
        r = requests.get('{0}{1}'.format(DISCOGS_MASTER, album.discogs_id), headers=HEADERS)
        result = r.json()
        for track in result.get('tracklist'):
            try:
                track = Track(title=track.get('title'),
                              duration=track.get('duration'),
                              position=track.get('position'))
                album.tracklist.append(track)
                db.session.add(track)
                db.session.commit()
            except:
                # TODO: remove later
                print(sys.exc_info())
                db.session.rollback()


@manager.command
def build_index():
    '''Index database'''
    models = [Album, Artist, Track]
    for model in models:
        print('Indexing {0} table... ({1}/{2})'.format(model.__tablename__,
                                                       models.index(model) + 1, len(models)))
        for entry in tqdm(model.query.all()):
            index = SearchIndex(search_text=entry.get_search_term(),
                                model_type=entry.__tablename__, object_id=entry.id)
            try:
                db.session.add(index)
                db.session.commit()
            except:
                db.session.rollback()
        print('Done')


manager.add_command('db', MigrateCommand)
manager.run()
