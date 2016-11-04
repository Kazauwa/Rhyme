from flask import render_template, redirect, url_for
from app import app, db
from .forms import SearchForm
from app.models import Album
# from config import HEADERS, DISCOGS_MASTER


@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html')
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.construct_query()
        return render_template('search.html', form=form, results=query)
    return render_template('search.html', form=form, results='There is none')


@app.route('/album/id<master_id>')
def album(master_id):
    result = db.Album.filter(Album.id == master_id)
    return render_template('album.html', result=result)
