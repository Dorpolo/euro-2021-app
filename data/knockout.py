import json
import requests
import environ
import os
from pathlib import Path
from data.teams import teams, teams_mock

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
BETA_MODE = True #TODO - Change once knockout starting


class BuildKnockOutForm:
    def __init__(self):
        self.TOKEN = env('API_TOKEN')
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'

    def extract_data(self, beta_mode: bool = False):
        if beta_mode:
            r = requests.get(url=self.URL.replace('_id=40', '_id=82'))
        else:
            r = requests.get(url=self.URL)
        data = json.loads(r.text)
        return data

    def get_api_data(self, beta_mode: bool = False) -> dict:
        metadata = {}
        data = self.extract_data(beta_mode)
        for item in data['calendar']['matchdays']:
            matches = item['matches']
            is_playoff = item['matchdayPlayoff']
            match_type = item['matchdayName']
            for sub_item in matches:
                game_id = sub_item['matchID']
                status = sub_item['matchStatus']['statusID']
                game_status = 'Fixture' if status == '0' else 'Live' if status == '-1' else 'Finished'
                home_team = sub_item['homeParticipant']['participantName']
                away_team = sub_item['awayParticipant']['participantName']
                real_score_home = sub_item['homeParticipant']['score']
                real_score_away = sub_item['awayParticipant']['score']
                metadata[game_id] = {
                    'status': game_status,
                    'match_label': f"{home_team}-{away_team}",
                    'real_score_home': real_score_home,
                    'real_score_away': real_score_away,
                    'score_label': f"{real_score_home} - {real_score_away}",
                    'direction': 1 if real_score_home > real_score_away else 2 if real_score_home < real_score_away else 0,
                    'date': sub_item['matchDate'],
                    'time': sub_item['matchTime'],
                    'game_id': game_id,
                    'is_playoff': is_playoff,
                    'match_type': match_type,
                    'home_team': home_team,
                    'away_team': away_team
                 }
        return metadata

    def get_knockout_matches(self) -> dict:
        data = {key: val for key, val in self.get_api_data(beta_mode=True).items()
                if val['is_playoff'] == '1' and val['match_type'] != '1/16 Final'}
        output = {}
        for item in [f"{j}Final" for j in ['1/8 ', '1/4 ', '1/2 ', '']]:
            output[item] = {}
            for key, val in data.items():
                if val['match_type'] == item:
                    output[item][val['game_id']] = {
                            'home': val['home_team'],
                            'away': val['away_team'],
                            'label': val['match_label'],
                            'date': val['date'],
                            'time': val['time']
                        }
        return output

    def get_knockout_team(self, beta_mode: bool = True) -> dict:
        if beta_mode:
            s_id, divider, team_dict = '82', 2, teams_mock
        else:
            s_id, divider, team_dict = '40', 1, teams
        URL = f"https://api.statorium.com/api/v1/matches/?season_id={s_id}&apikey={self.TOKEN}"
        data = requests.get(url=URL).json()
        output = {}
        playoff_matches = [item for item in data['calendar']['matchdays'] if item['matchdayPlayoff'] == '1']
        for item in playoff_matches:
            stage = item['matchdayName']
            if stage != '1/16 Final':
                output[stage] = {}
                i = 0
                stage_length = int(round((len(item['matches'])/divider) + 0.1))
                for sub_item in item['matches'][0:stage_length]:
                    output[stage][f"a{i}"] = {
                                    'home': {
                                        'name': sub_item['homeParticipant']['participantName'],
                                        'id': sub_item['homeParticipant']['participantID'],
                                        'image': team_dict[sub_item['homeParticipant']['participantName']]['logo']
                                    },
                                    'away': {
                                        'name': sub_item['awayParticipant']['participantName'],
                                        'id': sub_item['awayParticipant']['participantID'],
                                        'image': team_dict[sub_item['awayParticipant']['participantName']]['logo']
                                    }
                                }
                    i += 1
        return output

    def get_team_game_map(self):
        team_game_map = {}
        input_dict = self.get_knockout_team(beta_mode=BETA_MODE)
        for key, val in input_dict.items():
            team_game_map[key] = {}
            i = 0
            for sub_key, sub_val in val.items():
                if i <= 7:
                    team_game_map[key][f"gid_{sub_key}_0"] = sub_val['home']['name']
                    team_game_map[key][f"gid_{sub_key}_1"] = sub_val['away']['name']
                i += 1
        return team_game_map


GetAPI = BuildKnockOutForm()
KNOCK_OUT_MATCHES = GetAPI.get_knockout_matches()
KNOCK_OUT_LOGOS = GetAPI.get_knockout_team(beta_mode=BETA_MODE)
TEAM_GAME_MAP = GetAPI.get_team_game_map()
TOP_16 = tuple([((item['home'], item['home']), (item['away'], item['away'])) for item in KNOCK_OUT_MATCHES['1/8 Final'].values()][0:8])
TOP_8 = tuple([((item['home'], item['home']), (item['away'], item['away'])) for item in KNOCK_OUT_MATCHES['1/4 Final'].values()][0:8])
TOP_4 = tuple([((item['home'], item['home']), (item['away'], item['away'])) for item in KNOCK_OUT_MATCHES['1/2 Final'].values()][0:8])
TOP_2 = tuple([((item['home'], item['home']), (item['away'], item['away'])) for item in KNOCK_OUT_MATCHES['Final'].values()][0:8])

cup_meta = GetAPI.get_api_data().values()
qualification_labels = [item['match_label'] for item in cup_meta if item['match_type'] == '3rd Round']

CUP_GAMES = {
    'qualification_1': qualification_labels[0:6],
    'qualification_2': qualification_labels[6:],
    '1/8 Final': [item['match_label'] for item in cup_meta if item['match_type'] == '1/8 Final'],
    '1/4 Final': [item['match_label'] for item in cup_meta if item['match_type'] == '1/4 Final'],
    '1/2 Final': [item['match_label'] for item in cup_meta if item['match_type'] == '1/2 Final'],
    'Final': [item['match_label'] for item in cup_meta if item['match_type'] == 'Final']
}