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
    # access_token_params={'redirect_uri': 'http://52.57.140.78'},
    authorize_url='https://oauth.vk.com/authorize')

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/rhyme.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('rhyme startup')


from app import views, models
