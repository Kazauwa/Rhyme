import requests
import json
from flask import render_template, redirect, url_for, session
from app import app
from .forms import SearchForm
from config import HEADERS, DISCOGS_QUERY, DISCOGS_MASTER


@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html')
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        session['save_data'] = form.save_to_json.data
        return redirect(url_for('search_results', query=form.search_by_album.data))
    return render_template('search.html', form=form)


@app.route('/search_results/<query>/', methods=['GET', 'POST'])
def search_results(query):
    r = requests.get(DISCOGS_QUERY, params={'q': query, 'type': 'master'}, headers=HEADERS)
    result = {count + 1: {'id': result.get('id'),
                          'title': result.get('title'),
                          'genre': result.get('genre'),
                          'thumb': result.get('thumb'),
                          'year': result.get('year')} for count, result in enumerate(r.json()['results'])}
    if session['save_data']:
        with open('data.json', 'a') as writer:
            for key, value in result.items():
                json.dump({key: value}, writer)
                writer.write('\n')
    return render_template('search_results.html',
                            query=query,
                            results=result.values())


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
