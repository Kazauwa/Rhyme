from flask import render_template, redirect, url_for, request, session, g, flash
from flask_oauthlib.client import OAuthException
from flask_login import login_required, login_user, current_user, logout_user
from app import app, vk, db, lm
from .forms import SearchForm, EditForm
from .models import SearchIndex, User, Album, Artist


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    g.search_form = SearchForm()


@vk.tokengetter
def get_vk_oauth_token(token=None):
    return session.get('oauth_token')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if g.search_form.validate_on_submit():
        method = getattr(SearchIndex, request.form['options'])
        query = method(g.search_form.data.get('search'))
        if query is None:
            flash('Your query returned no results. Try changing your query.')
        return render_template('search.html', results=query, option=request.form['options'])
    flash('Input some data in order to perform search')
    return render_template('search.html', results=None)


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
        me = vk.request('users.get', data={'access_token': resp['access_token'],
                                           'fields': 'sex,photo_200,photo_100,domain'})
        me = me.data['response'][0]
        user = User(vk_id=me.get('uid'),
                    first_name=me.get('first_name'),
                    last_name=me.get('last_name'),
                    nickname=me.get('domain'),
                    sex=me.get('sex'),
                    profile_pic=me.get('photo_200'),
                    thumb=me.get('photo_100'))
        db.session.add(user)
        db.session.commit()
    login_user(user)
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


@app.route('/user/<nickname>/follow')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User {0} not found.'.format(nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow {0}!'.format(nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following {0}!'.format(nickname))
    return redirect(url_for('user', nickname=nickname))


@app.route('/user/<nickname>/unfollow')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User {0} not found.'.format(nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow {0}!'.format(nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following {0}'.format(nickname))
    return redirect(url_for('user', nickname=nickname))


@app.route('/album/id<int:id>')
def album(id):
    album = Album.query.get(id)
    artist = Artist.query.get(album.artist_id)
    return render_template('album.html', result=album, artist=artist)


@app.route('/album/id<int:id>/add')
@login_required
def add_album(id):
    album = Album.query.get(id)
    if album is None:
        flash('Album not found!')
        return redirect(url_for('index'))
    a = g.user.add_album(album)
    if a is None:
            flash('Can\'t add album!')
            return redirect(url_for('album', id=id))
    db.session.add(a)
    db.session.commit()
    flash('Album successfully added!')
    return redirect(url_for('album', id=id))


@app.route('/album/id<int:id>/remove')
@login_required
def remove_album(id):
    album = Album.query.get(id)
    if album is None:
        flash('Album not found!')
        return redirect(url_for('index'))
    a = g.user.remove_album(album)
    if a is None:
            flash('Can\'t remove album!')
            return redirect(url_for('album', id=id))
    db.session.add(a)
    db.session.commit()
    flash('Album successfully removed!')
    return redirect(url_for('album', id=id))


@app.route('/artist/id<int:id>')
@login_required
def artist(id):
    artist = Artist.query.get(id)
    return render_template('artist.html', result=artist)
