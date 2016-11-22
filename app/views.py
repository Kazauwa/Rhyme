from flask import render_template, redirect, url_for, request, session, g, flash
from flask_oauthlib.client import OAuthException
from flask_login import login_required, login_user, current_user, logout_user
from app import app, vk, db, lm
from .forms import SearchForm, EditForm
from .models import SearchIndex, User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@vk.tokengetter
def get_vk_oauth_token(token=None):
    return session.get('oauth_token')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    #return redirect(url_for('search', filter=None))
    #return redirect(url_for('login'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        query = SearchIndex.search_album(form.data.get('search'))
        return render_template('search.html', form=form, results=query)
    return render_template('search.html', form=form, results=None)


@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        return 'You are already logged in!'
    callback = url_for(
        'vk_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True)
    return vk.authorize(callback=callback)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login/authorized')
def vk_authorized():
    resp = vk.authorized_response()
    if resp is None:
        return 'Access denied: reason={0} error={1}'.format(request.args['error_reason'],
                                                            request.args['error_description'])
    if isinstance(resp, OAuthException):
        return 'Access denied: {0}'.format(resp.message)
    session['oauth_token'] = (resp['access_token'], '')
    user = User.query.filter_by(vk_id=resp['user_id']).first()
    if not user:
        me = vk.request('users.get', data={'access_token': resp['access_token'], 'fields': 'sex,photo_max_orig,domain'})
        me = me.data['response'][0]
        user = User(vk_id=me.get('uid'),
                    first_name=me.get('first_name'),
                    last_name=me.get('last_name'),
                    nickname=me.get('domain'),
                    sex=me.get('sex'),
                    profile_pic=me.get('photo_max_orig'))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('Logged in as {0}'.format(user.nickname))
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User {0} not found'.format(nickname))
        return redirect(url_for('index'))
    return render_template('user.html', user=user)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
    return render_template('edit.html', form=form)
