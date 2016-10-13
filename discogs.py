import os
import requests
import json

TOKEN = os.environ.get('DISCOGS_TOKEN')

headers = {'Authorization': 'Discogs token=' + TOKEN, 'User-Agent': 'RhymeApp/0.1'}
query = 'Strange Days'
params = {'query': query, 'type': 'master'}
URL = 'https://api.discogs.com/database/search'

r = requests.get(URL, params=params, headers=headers)

result = {count + 1: {'id': result.get('id'),
                      'title': result.get('title'),
                      'genre': result.get('genre'),
                      'thumb': result.get('thumb'),
                      'year': result.get('year')} for count, result in enumerate(r.json()['results'])}

with open('data.json', 'a') as writer:
    for key, value in result.items():
        json.dump({key: value}, writer)
        writer.write('\n')
