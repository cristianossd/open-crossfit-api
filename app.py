import requests
import json

from flask import Flask
app = Flask(__name__)

AFFILIATES_ENDPOINT = 'https://map.crossfit.com/ac'

@app.route('/', methods=['GET'])
def get_affiliates():
    params = {'term': 'crossfit'}
    r = requests.get(AFFILIATES_ENDPOINT, params=params)

    if r.status_code == 200:
        affiliates_fn = lambda a: a['state'] == 'Bahia' and a['country'] == 'Brazil'
        state_affiliates = list(filter(affiliates_fn, r.json()))

        print(state_affiliates)

    return 'ok'
