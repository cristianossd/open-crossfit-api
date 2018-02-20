from flask import Flask

import requests
import json

# configuration

SECRET_KEY='259303671668505404683084822181292439349L'

# create api
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('OPENCROSSFITAPI_SETTINGS', silent=True)

# routes constants

AFFILIATES_ENDPOINT = 'https://map.crossfit.com/ac'
AFFILIATES_FILE = 'opencrossfitapi/static/db/affiliates.json'
ATHLETES_ENDPOINT = 'https://games.crossfit.com/competitions/api/v1/competitions/open/2018/leaderboards'
ATHLETES_FILE = lambda sex: 'opencrossfitapi/static/db/%s_athletes.json' % sex

@app.route('/affiliates/<string:country>/<string:state>', methods=['GET'])
def get_affiliates(country, state):
    params = {'term': 'crossfit'}
    r = requests.get(AFFILIATES_ENDPOINT, params=params)

    affiliates_num = 0

    if r.status_code == 200:
        affiliates_fn = lambda a: a['state'] == state and a['country'] == country
        state_affiliates = list(filter(affiliates_fn, r.json()))

        with open(AFFILIATES_FILE, 'w') as f:
            json.dump(state_affiliates, f)

        affiliates_num = len(state_affiliates)

    return 'Found %d affiliates in %s\n' %(affiliates_num, state)

@app.route('/athletes', methods=['GET'])
def get_athletes():
    leaderboard_key = 'leaderboardRows'
    men_athletes = []
    women_athletes = []
    men_params = {'division': 1, 'scaled': 0}
    women_params = {'division': 2, 'scaled': 0}

    with open(AFFILIATES_FILE, 'r') as json_data:
        affiliates = json.load(json_data)

        for affiliate in affiliates:
            print('[%s] Men athletes' % affiliate['0'])
            men = []

            men_params['affiliate'] = affiliate['5']
            r = requests.get(ATHLETES_ENDPOINT, params=men_params)
            if leaderboard_key in r.json():
                men = list(map(mount_athlete, r.json()[leaderboard_key]))
                for a in men: print(a['competitorName'])

                men_athletes = men_athletes + men

            print('[%s] Women athletes' % affiliate['0'])
            women = []

            women_params['affiliate'] = affiliate['5']
            r = requests.get(ATHLETES_ENDPOINT, params=women_params)
            if leaderboard_key in r.json():
                women = list(map(mount_athlete, r.json()[leaderboard_key]))
                for a in women: print(a['competitorName'])

                women_athletes = women_athletes + women

            print()

        with open(ATHLETES_FILE('men'), 'w') as f:
            json.dump(men_athletes, f)

        with open(ATHLETES_FILE('women'), 'w') as f:
            json.dump(women_athletes, f)

    return 'Found %d athletes in Bahia\n' % (len(men_athletes) + len(women_athletes))

# could this method be protected?
def mount_athlete(athlete):
    new_athlete = athlete['entrant']
    new_athlete['scores'] = athlete['scores']

    return new_athlete
