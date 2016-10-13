import requests
import operator
import pandas as pd

params = {'uid': '152064949',
          'access_token': '81ba53c62678b652bdacd818e96fec29de5533006ea4a5d4f24a9254d2a28f93542f59e18f072f8748881'}
r = requests.get('https://api.vk.com/method/audio.get', params=params)
response = r.json()['response']
freq = dict()
for track in response:
    if track['artist'].lower() not in freq:
        freq[track['artist'].lower()] = 0
    freq[track['artist'].lower()] += 1

sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
top_freq = pd.DataFrame(sorted_freq[:10], columns=['Artist', 'Occurances'], index=range(1, 11))
top_freq.plot.bar()
