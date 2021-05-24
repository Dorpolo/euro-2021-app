import requests
import json
import environ
import os
from pathlib import Path
from data.teams import teams

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class EuroApi:
    def __init__(self):
        self.TOKEN = env('API_TOKEN')
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'

    def extract_data(self):
        r = requests.get(url=self.URL)
        data = json.loads(r.text)
        return data

    def read_fixtures(self):
        data = self.extract_data()
        fixtures_list = []
        for item in data['calendar']['matchdays']:
            for key, value in item.items():
                if key == 'matches':
                    for item2 in value:
                        game_id = item2['matchID']
                        home_team_id = item2['homeParticipant']['participantID']
                        away_team_id = item2['awayParticipant']['participantID']
                        home_team = item2['homeParticipant']['participantName']
                        away_team = item2['awayParticipant']['participantName']
                        txt = f'{home_team} - {away_team}'
                        fixtures_list.append(txt)
        return fixtures_list

    def main(self):
        output = self.read_fixtures()
        return output

