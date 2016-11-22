from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from config import VK_APP_ID, VK_APP_SECRET


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
lm = LoginManager()
lm.init_app(app)
oauth = OAuth(app)

vk = oauth.remote_app(
    'vk',
    consumer_key=VK_APP_ID,
    consumer_secret=VK_APP_SECRET,
    request_token_params={'scope': 'friends,audio,offline'},
    base_url='https://api.vk.com/method/',
    request_token_url=None,
    access_token_url='https://oauth.vk.com/access_token',
    access_token_method='GET',
    authorize_url='https://oauth.vk.com/authorize')

from app import views, models
