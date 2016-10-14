import os

# Global parameters
WTF_CSRF_ENABLED = False
SECRET_KEY = os.environ.get('FLASK_SECRET')

# Discogs
TOKEN = os.environ.get('DISCOGS_TOKEN')
HEADERS = {'Authorization': 'Discogs token=' + TOKEN, 'User-Agent': 'RhymeApp/0.1'}
DISCOGS_API = 'https://api.discogs.com/database/search'
