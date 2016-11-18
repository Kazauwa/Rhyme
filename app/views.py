from flask import render_template, redirect, url_for
from app import app
from .forms import SearchForm
from .models import SearchIndex


@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html')
    return redirect(url_for('search', filter=None))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = SearchIndex.search_album(form.data.get('search'))
        return render_template('search.html', form=form, results=query)
    return render_template('search.html', form=form, results=None)
