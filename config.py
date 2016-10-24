import os

# Global parameters
WTF_CSRF_ENABLED = False
SECRET_KEY = os.environ.get('FLASK_SECRET')
BASEDIR = os.path.abspath(os.path.dirname(__name__))

# Discogs
TOKEN = os.environ.get('DISCOGS_TOKEN')
HEADERS = {'Authorization': 'Discogs token=' + TOKEN, 'User-Agent': 'RhymeApp/0.1'}
DISCOGS_QUERY = 'https://api.discogs.com/database/search'
DISCOGS_MASTER = 'https://api.discogs.com/masters/'

# VK
APP_ID = os.environ.get('VK_APP_ID')

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
