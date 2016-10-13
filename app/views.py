import requests
import operator
from collections import Counter
from flask import render_template, redirect
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/<user_id>/<access_token>')
def audio(user_id=None, access_token=None):
    if user_id is None or access_token is None:
        return redirect(url_for('index'))
    params = {'uid': user_id, 'access_token': access_token}
    response = requests.get('https://api.vk.com/method/audio.get', params=params)
    response = response.json()['response']
    audio = Counter()
    for track in response:
        audio[track['artist'].lower()] += 1
    audio = sorted(audio.items(), key=operator.itemgetter(1), reverse=True)
    return render_template('bar.html',
                            audio=audio[:11],
                            user=user_id)
