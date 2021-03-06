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
                filtered_men = list(filter(lambda a: a != None, men))
                for a in filtered_men: print(a['competitorName'])

                men_athletes = men_athletes + filtered_men

            print('[%s] Women athletes' % affiliate['0'])
            women = []

            women_params['affiliate'] = affiliate['5']
            r = requests.get(ATHLETES_ENDPOINT, params=women_params)
            if leaderboard_key in r.json():
                women = list(map(mount_athlete, r.json()[leaderboard_key]))
                filtered_women = list(filter(lambda a: a != None, women))
                for a in filtered_women: print(a['competitorName'])

                women_athletes = women_athletes + filtered_women

            print()

        with open(ATHLETES_FILE('men'), 'w') as f:
            sorted_men = list(sorted(men_athletes, key=lambda a: a['scores'][0]))
            json.dump(sorted_men, f)

        with open(ATHLETES_FILE('women'), 'w') as f:
            sorted_women = list(sorted(women_athletes, key=lambda a: a['scores'][0]))
            json.dump(sorted_women, f)

    return 'Found %d athletes in Bahia\n' % (len(men_athletes) + len(women_athletes))

def mount_athlete(athlete):
    try:
        new_athlete = athlete.get('entrant')
        new_athlete['scores'] = athlete.get('scores')

        # 18.1
        new_athlete['scores'][0] = build_18_1(new_athlete.get('scores')[0])

        return new_athlete
    except:
        return

def build_18_1(score):
    if score['scaled'] == '1':
        print('SACALED!!')
        raise Exception('Scaled')

    new_score = {
        'score': score.get('score'),
        'scoreDisplay': score.get('scoreDisplay')
    }

    return new_score
