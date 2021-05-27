import requests
import json
import environ
import os
from pathlib import Path
from data.teams import teams, groups

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
            for sub_item in item['matches']:
                game_id = sub_item['matchID']
                home_team_id = sub_item['homeParticipant']['participantID']
                away_team_id = sub_item['awayParticipant']['participantID']
                home_team = sub_item['homeParticipant']['participantName']
                away_team = sub_item['awayParticipant']['participantName']
                home_logo = teams[home_team]['logo']
                away_logo = teams[away_team]['logo']
                home_score = sub_item['homeParticipant']['score']
                away_score = sub_item['awayParticipant']['score']
                group = groups[home_team]['groupName']
                matchdayID = item['matchdayID']
                match_day = item['matchdayName']
                match_date = sub_item['matchDate']
                match_time = sub_item['matchTime']
                home_row = [0, game_id, group, match_day, match_date, match_time, home_team_id, home_team, home_logo, home_score]
                away_row = [1, game_id, group, match_day, match_date, match_time, away_team_id, away_team, away_logo, away_score]
                fixtures_list.append(home_row)
                fixtures_list.append(away_row)
        return fixtures_list

    @staticmethod
    def dynamic_sort(sub_li):
        sub_li.sort(key=lambda x: [x[2], x[3], x[4], x[5], x[1], x[0]])
        return sub_li

    def get_unique_teams(self):
        output = self.read_fixtures()
        team_list = [item[8] for item in output]
        return set(team_list)

    def main(self):
        output = self.read_fixtures()
        return self.dynamic_sort(output)