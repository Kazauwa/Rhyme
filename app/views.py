from flask import render_template, redirect, url_for, request, session
from flask_oauthlib.client import OAuthException
from app import app, vk
from .forms import SearchForm
from .models import SearchIndex


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    #return redirect(url_for('search', filter=None))
    #return redirect(url_for('login'))


@vk.tokengetter
def get_vk_oauth_token(token=None):
    return session.get('oauth_token')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = SearchIndex.search_album(form.data.get('search'))
        return render_template('search.html', form=form, results=query)
    return render_template('search.html', form=form, results=None)


@app.route('/login')
def login():
    callback = url_for(
        'vk_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True)
    return vk.authorize(callback=callback)


@app.route('/login/authorized')
def vk_authorized():
    resp = vk.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(request.args['error_reason'],
                                                            request.args['error_description'])
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)
    session['oauth_token'] = (resp['access_token'], '')
    me = vk.request('users.get', data={'access_token': resp['access_token'], 'fields': 'sex,bdate,photo_max_orig'})
    return 'Logged in as {0}'.format(me.data)
