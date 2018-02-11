import requests

from flask import Flask
app = Flask(__name__)

AFFILIATES_ENDPOINT = 'https://map.crossfit.com/ac'

@app.route('/', methods=['GET'])
def get_affiliates():
    params = {'term': 'crossfit'}
    r = requests.get(AFFILIATES_ENDPOINT, params=params)

    print(r.status_code)

    return 'ok'
