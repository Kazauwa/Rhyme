import os

# Global parameters
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get('FLASK_SECRET')
BASEDIR = os.path.abspath(os.path.dirname(__name__))
DEBUG = True

# Discogs
TOKEN = os.environ.get('DISCOGS_TOKEN')
HEADERS = {'Authorization': 'Discogs token=' + TOKEN, 'User-Agent': 'RhymeApp/0.1'}
DISCOGS_QUERY = 'https://api.discogs.com/database/search'
DISCOGS_MASTER = 'https://api.discogs.com/masters/'

# VK
APP_ID = os.environ.get('VK_APP_ID')

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
