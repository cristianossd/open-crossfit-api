import requests
import json

from flask import Flask
app = Flask(__name__)

AFFILIATES_ENDPOINT = 'https://map.crossfit.com/ac'
AFFILIATES_FILE = 'static/db/affiliates.json'

@app.route('/', methods=['GET'])
def get_affiliates():
    params = {'term': 'crossfit'}
    r = requests.get(AFFILIATES_ENDPOINT, params=params)

    affiliates_num = 0

    if r.status_code == 200:
        affiliates_fn = lambda a: a['state'] == 'Bahia' and a['country'] == 'Brazil'
        state_affiliates = list(filter(affiliates_fn, r.json()))

        with open(AFFILIATES_FILE, 'w') as f:
            json.dump(state_affiliates, f)

        affiliates_num = len(state_affiliates)

    return 'Found %d affiliates in Bahia\n' % affiliates_num
