import requests
from flask import render_template, redirect, url_for, request
from app import app, db
from .forms import SearchForm
from app.models import Album, Track, Artist
from config import HEADERS, DISCOGS_MASTER


def construct_query(data):
    #query = db.session.query(*form.to_dict().keys())
    #if form.search_by_album.data:
        #    query = query.filter(Album.title == form.search_by_album.data)
    #if form.search_by_artist.data:
        #    query = query.filter(Artist.name == form.search_by_artist.data)
    #if form.search_track.data:
        #    query = query.filter(Track.title == form.search_track.data)
    #if form.year.data:
        #    query = query.filter(Album.year == form.year.data)
    #result = query.all()
    pass


@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html')
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        construct_query(form.data)
        return render_template('search.html', form=form, results=request.args)
    return render_template('search.html', form=form, results='There is none')


@app.route('/album/id<master_id>')
def album(master_id):
    r = requests.get(DISCOGS_MASTER + str(master_id), headers=HEADERS)
    result = {'styles': r.json().get('styles'),
              'genres': r.json().get('genres'),
              'title': r.json().get('title'),
              'artists': r.json().get('artists'),
              'year': r.json().get('year'),
              'images': r.json().get('images'),
              'tracklist': r.json().get('tracklist')}
    return render_template('album.html', result=result)
