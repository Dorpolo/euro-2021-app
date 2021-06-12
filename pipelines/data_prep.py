from data.teams import team_game_map
from myapp.models import *
import plotly.graph_objects as go
import numpy as np
from myproject.settings import MEDIA_URL, AWS_S3_URL, DEFAULT_PHOTO
from collections import defaultdict
import pandas as pd
import requests
import environ
import os
from pathlib import Path
from data.teams import teams, groups
import json
import data.viz_variables as vis
import plotly.express as px
import plotly.offline as opy

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


def prepare_bet_submission_email(request, form) -> dict:
    home, away, results = [], [], []
    top_players = {}

    for i in enumerate([(key, obj) for key, obj in form.cleaned_data.items() if key != 'user_name']):
        if 'top_' in i[1][0]:
            top_players[i[1][0]] = i[1][1]
        else:
            if i[0] % 2 == 0:
                home.append(i[1])
            else:
                away.append(i[1])
    for h, a in zip(home, away):
        result = f"{team_game_map[h[0]]}-{team_game_map[a[0]]}: {h[1]}-{a[1]}"
        results.append(result)
    text_results = '\n'.join(results)
    player_list = [f"{key}: {obj}" for key, obj in top_players.items()]
    player_joined = '\n'.join(player_list)
    subject = "Euro 2021 Friends League - Email Confirmation - Bet Submission"
    message = f"Dear {request.user.username}!\n" \
              f"You have just submitted successfully your bet form!\n" \
              f"Please Note - you can easily edit your bets by 2021-07-09 at 11:59:59 PM using the app 'edit your bet' tab.\n\n" \
              f"For your convenience and our documentation, please find bellow your bets. \n\n" \
              f"{text_results}\n\n" \
              f"{player_joined}\n\n" \
              "Regards,\nLeague management team"
    return {'subject': subject, 'message': message}


def prepare_league_user_email(request, form) -> dict:
     subject = "Euro 2021 Friends League - Email Confirmation - League Membership"
     message = f"Dear {form.cleaned_data['first_name']}!\n" \
               f"You are officially part of the {form.cleaned_data['league_name']} league. " \
               f"Please make sure to submit your bets. Good luck!\n\n" \
               "Regards,\nLeague management team"
     return {'subject': subject, 'message': message}


def get_league_user_email(user) -> str:
    data = LeagueMember.objects.filter(user_name_id=user)
    return data[0].email


def extract_user_league_name_id(user: int) -> tuple:
    league_member_data = list(LeagueMember.objects.filter(user_name_id=user).values())
    leagues = [item['league_name_id'] for item in league_member_data]
    if len(leagues) > 0:
        return True, leagues
    else:
        return False, None


def extract_league_users(user) -> tuple:
    league_ids = extract_user_league_name_id(user)
    if league_ids[0]:
        user_list = {}
        for item in league_ids[1]:
            data = list(LeagueMember.objects.filter(league_name_id=item).values())
            for obj in data:
                user_list[item] = obj
        return True, user_list
    else:
        return False, None


def extract_league_bets(user):
    league_users = extract_league_users(user)
    if league_users[0]:
        unique_users = [item['user_name_id'] for item in league_users[1].values()]
        data = list(Game.objects.all().values())
        filtered_data = [item for item in data if item['user_name_id'] in unique_users]
        return filtered_data
    else:
        return None


def user_onboarding(user) -> dict:
    league_data = LeagueMember.objects.filter(user_name_id=user)
    bet_data = Game.objects.filter(user_name_id=user)
    image = UserImage.objects.filter(user_name_id=user)
    league_assigned = True if len(league_data) > 0 else False
    bet_assigned = True if len(bet_data) > 0 else False
    image_uploaded = True if len(image) > 0 else False
    return {'league': league_assigned, 'bet': bet_assigned, 'image': image_uploaded}


def user_game_bet_id(user) -> dict:
    data = Game.objects.filter(user_name_id=user)
    if len(data) > 0:
        return data[0].id
    else:
        return None


def get_league_member_id(user) -> dict:
    data = LeagueMember.objects.filter(user_name_id=user)
    if len(data) > 0:
        league_data = list(data.values())
        output = {}
        for item in league_data:
            output[item['league_name_id']] = item['id']
        return output
    else:
        return None


def get_user_image(user) -> dict:
    data = UserImage.objects.filter(user_name_id=user)
    if len(data) > 0:
        return data[0].header_image
    else:
        return None


def get_league_name() -> tuple:
   data = League.objects.all()
   leagues = []
   for j in range(len(data)):
       leagues.append(data[j].league_name)
   unique_leagues = set(leagues)
   league_list = [(item, item) for item in unique_leagues]
   return tuple(league_list)


def get_league_member_data(user_id: int):
    league_name_id = extract_user_league_name_id(user_id)
    if league_name_id[0]:
        league_data_output = []
        for obj in league_name_id[1]:
            league_users = list(LeagueMember.objects.filter(league_name_id=obj).values())
            league_users_dict = {item['user_name_id']: item for item in league_users}
            user_image = list(UserImage.objects.all().values())
            user_image_dict = {item['user_name_id']: item['header_image'] for item in user_image}
            user_id_with_images = [item for item in user_image_dict.keys()]
            for member in league_users:
                user_id = member['user_name_id']
                if user_id in user_id_with_images:
                    league_users_dict[user_id]['image'] = f"{AWS_S3_URL}{user_image_dict[user_id]}"
                else:
                    league_users_dict[user_id]['image'] = f"{AWS_S3_URL}{DEFAULT_PHOTO}"
            league_data_output_unit = [item for item in league_users_dict.values()]
            league_data_output.append(league_data_output_unit)
        meta = {}
        for item in league_data_output:
            league_name = item[0]['league_name_id']
            meta[league_name] = []
            for sub_item in item:
                meta[league_name].append([sub_item['nick_name'], sub_item['image']])
        return meta
    else:
        return None


class EuApi:
    def __init__(self, user_id):
        self.TOKEN = env('API_TOKEN')
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'
        self.user_id = user_id

    def extract_data(self):
        r = requests.get(url=self.URL)
        data = json.loads(r.text)
        return data


class UpdateUserPrediction:
    def __init__(self, user_id):
        self.TOKEN = env('API_TOKEN')
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'
        self.user_id = user_id

    def extract_data(self):
        r = requests.get(url=self.URL)
        data = json.loads(r.text)
        return data

    def get_api_data(self) -> dict:
        metadata = {}
        data = self.extract_data()
        for item in data['calendar']['matchdays']:
            matches = item['matches']
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
                    'game_id': game_id
                 }
        return metadata

    @staticmethod
    def get_user_prediction():
        df_init = pd.DataFrame(list(Game.objects.all().values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('top_')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home', 'Away')
        df['game_id'] = df.variable.str[4:-2]
        df['predicted_score'] = df['value'].astype(str)
        df_main = df.sort_values(by=['user_name_id', 'variable', 'location']).groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[[0, 1]]
        return df_main

    def data_enrichment(self):
        extra_fields = ['game_id', 'match_label', 'real_score', 'real_score_home', 'real_score_away', 'game_status', 'date', 'hour']
        df_main = self.get_user_prediction()
        metadata = self.get_api_data()
        more_data = [[
             id,
             metadata[id]['match_label'],
             metadata[id]['score_label'],
             metadata[id]['real_score_home'],
             metadata[id]['real_score_away'],
             metadata[id]['status'],
             metadata[id]['date'],
             metadata[id]['time'],
        ] for id in df_main.game_id.unique()]
        df_more_data = pd.DataFrame(more_data)
        df_more_data.columns = extra_fields
        df_main_2 = pd.merge(
                    df_main,
                    df_more_data,
                    on=['game_id'],
                    how='inner')
        league_member_fields = ['user_name_id', 'first_name', 'last_name', 'league_name_id', 'nick_name', 'created']
        df_league_member_pre = pd.DataFrame(list(LeagueMember.objects.all().values()))[league_member_fields].\
            sort_values(by=['user_name_id', 'league_name_id', 'created'], ascending=[True, True, False])
        df_league_member = df_league_member_pre.groupby(['user_name_id', 'league_name_id']).first().\
            reset_index().drop(columns='created')
        output = pd.merge(
                    df_main_2,
                    df_league_member,
                    on=['user_name_id'],
                    how='inner'
                ).sort_values(by=['date', 'hour', 'user_name_id'])
        output['user_full_name'] = output['first_name'] + ' ' + output['last_name']
        output['record_id'] = output['user_name_id'].astype(str) + '-' + output['match_label'] + '-' + output['league_name_id']
        output['date'] = output['date'].str[5:]
        output_fields = [
            'record_id',
            'user_name_id',
            'nick_name',
            'league_name_id',
            'match_label',
            'predicted_score',
            'real_score',
            'game_status',
            'date',
            'hour',
            'pred_score_home',
            'pred_score_away',
            'real_score_home',
            'real_score_away'
            ]
        return output[output_fields]

    def present_predictions(self):
        data = self.data_enrichment()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        if len(leagues) > 0:
            output = {}
            for item in leagues:
                required_fields = ['nick_name', 'date', 'hour', 'match_label', 'predicted_score', 'real_score',
                                   'game_status', 'pred_score_home', 'pred_score_away', 'real_score_home',
                                   'real_score_away', 'user_name_id']
                # & (data.user_name_id == self.user_id)
                filtered_df = data[(data.league_name_id == item)][required_fields]
                output[item] = filtered_df.values.tolist()
            return output, required_fields
        else:
            return None, None

    @staticmethod
    def table_calculations(x):
        x['pred_dir'] = np.where(x.pred_score_home > x.pred_score_away, 'home', np.where(x.pred_score_home < x.pred_score_away, 'away', 'draw'))
        x['real_dir'] = np.where(x.real_score_home > x.real_score_away, 'home', np.where(x.real_score_home < x.real_score_away, 'away', 'draw'))
        x['is_direction'] = np.where(x.pred_dir == x.real_dir, 1, 0)
        x['is_boom'] = np.where((x.pred_score_home == x.real_score_home) & (x.pred_score_away == x.real_score_away), 1, 0)
        x['points'] = np.where(x.is_boom == 1, 3, np.where(x.is_direction == 1, 1, 0))
        x['started'] = np.where(x.game_status != 'Fixture', 1, 0)
        x['is_live'] = np.where(x.game_status == 'live', 1, 0)
        d = [
            int(x['started'].sum()),
            int((x['started'] * x['points']).sum()),
            int((x['started'] * x['is_boom'] * 3).sum()),
            int((x['started'] * x['is_direction']).sum()),
            round((x['started'] * x['points']).sum()*100/(x['started'] * 3).sum(), 1),
            int((x['started'] * x['is_boom'] * (x['pred_score_home'].astype(int) + x['pred_score_away'].astype(int))).sum()),
            int((x['is_live'] * x['points']).sum()),
        ]
        index_names = ['games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'live_points']
        return pd.Series(d, index=[index_names])

    def get_game_points_group_stage(self, df) -> tuple:
        data = df.groupby(['user_name_id', 'nick_name']).apply(self.table_calculations).\
            reset_index().drop(columns=['user_name_id']).sort_values(
                    by=[('points',), ('boom',), ('direction', ), ('predicted_goals', )], ascending=[False]*4
                    )
        data['rn'] = np.arange(len(data)) + 1
        return data.values.tolist()

    def get_game_points_knockout(self) -> tuple:
        pass

    def get_game_points_players(self) -> tuple:
        pass

    def league_member_points(self):
        metadata = self.present_predictions()
        output = {}
        if metadata[0] is not None:
            for key, obj in metadata[0].items():
                df = pd.DataFrame(obj)
                df.columns = metadata[1]
                output[key] = self.get_game_points_group_stage(df)
            return output
        else:
            return None


class EuMatch:
    def __init__(self):
        self.TOKEN = 'bfa132288504de6860c8ae3259d21fa7'
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'

    def extract_data(self):
        data = requests.get(url=self.URL).json()
        return data

    def all_matches(self):
        data = self.extract_data()
        output = []
        for item in data['calendar']['matchdays']:
            match_day_id = item['matchdayID']
            match_round = item['matchdayName']
            match_day_playoff = item['matchdayPlayoff']
            match_day_type = item['matchdayType']
            match_day_start = item['matchdayStart']
            match_day_end = item['matchdayEnd']
            for subitem in item['matches']:
                match_id = subitem['matchID']
                match_status = subitem['matchStatus']['statusID']
                match_date = subitem['matchDate']
                match_hour = subitem['matchTime']
                home_team = subitem['homeParticipant']['participantName']
                home_team_id = subitem['homeParticipant']['participantID']
                home_team_score = subitem['homeParticipant']['score']
                away_team = subitem['awayParticipant']['participantName']
                away_team_id = subitem['awayParticipant']['participantID']
                away_team_score = subitem['awayParticipant']['score']
                match_label = f"{home_team}-{away_team}"
                row = [match_day_id, match_round, match_day_playoff, match_day_type, match_day_start,
                       match_day_end, match_id, match_status, match_date, match_hour, home_team, home_team_id,
                       home_team_score, away_team, away_team_id, away_team_score, match_label]
                output.append(row)
        fields = ['match_day_id', 'match_round', 'match_day_playoff', 'match_day_type', 'match_day_start',
                  'match_day_end', 'match_id', 'match_status', 'match_date', 'match_hour', 'home_team',
                  'home_team_id', 'home_team_score', 'away_team', 'away_team_id', 'away_team_score','match_label']
        return output, fields

    def next_match(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        output = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
        return output.head(1).reset_index()

    def next_match_logos(self):
        next_teams = self.next_match()
        home = teams[next_teams.home_team[0]]['logo']
        away = teams[next_teams.away_team[0]]['logo']
        return {next_teams.home_team[0]: home, next_teams.away_team[0]: away}


class StatsNextGame(UpdateUserPrediction):
    def __init__(self, user_id, match_label):
        super().__init__(user_id)
        self.match_label = match_label

    def next_match_prediction_df(self):
        df_input = self.present_predictions()
        output = {}
        if df_input[0] is not None:
            for key, obj in df_input[0].items():
                df = pd.DataFrame(obj)
                df.columns = df_input[1]
                df = df[df.match_label == self.match_label]
                df[['home_team', 'away_team']] = df.match_label.str.split('-', expand=True, n=1)[[0, 1]]
                df['pred_dir'] = np.where(df.pred_score_home > df.pred_score_away,
                                          df.home_team, np.where(df.pred_score_home < df.pred_score_away, df.away_team, 'Draw'))
                df['predicted_score_alternative'] = np.where(df['pred_dir'] == df.away_team,
                                                             df['pred_score_away'] + '-' + df['pred_score_home'],
                                                             df['predicted_score'])
                df_scores = pd.DataFrame(df.groupby(['predicted_score_alternative', 'pred_dir'])['game_status'].count()).reset_index().\
                    rename(columns={
                            'game_status': 'count',
                            'predicted_score_alternative': 'score',
                            'pred_dir': 'winner'
                        }).merge(vis.SCORE_MAP_DF, on='score', how='inner')
                df_fig = df_scores.sort_values(by=['score_rank', 'winner'])
                output[key] = df_fig
            return output
        else:
            return None

    def next_match_winner_df(self):
        df_input = self.present_predictions()
        output = {}
        if df_input[0] is not None:
            for key, obj in df_input[0].items():
                df_winner = pd.DataFrame(obj.groupby(['pred_dir'])['game_status'].count()).\
                    reset_index().rename(columns={
                        'game_status': 'count',
                        'pred_dir': 'winner'
                    })
                df_winner_output = df_winner.sort_values(by=['winner_rank'])
                output[key] = df_winner_output
            return output
        else:
            return None

    def next_match_live_game(self):
        df_input = self.present_predictions()
        output = {}
        if df_input[0] is not None:
            for key, obj in df_input[0].items():
                df = pd.DataFrame(obj)
                df.columns = df_input[1]
                df = df[df.match_label == self.match_label]
                df[['home_team', 'away_team']] = df.match_label.str.split('-', expand=True, n=1)[[0, 1]]
                output[key] = obj
            return output
        else:
            return None

    @staticmethod
    def next_match_prediction_plot(data):
        fig = px.bar(data, x='score', y='count', color="winner", template='simple_white', text='count',
                     title="Score Distribution",  labels={"score": "Score", "count": "Prediction Count", "winner": ""})
        fig.update_traces(textposition='inside')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT,)
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def next_match_winner_plot(data):
        fig = px.pie(data, values='count', names='winner', title='Predicted Winner')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT,)
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def merge_dicts(a: dict, b: dict):
        new_output = {}
        for i, j in zip(a.items(), b.items()):
            if i[0] == j[0]:
                new_output[i[0]] = [i[1], j[1]]
        return new_output

    def next_match_prediction_outputs(self):
        dict_score = self.next_match_prediction_df()
        dict_winner = self.next_match_prediction_df()
        if dict_score is not None:
            output_score = {key: self.next_match_prediction_plot(data) for key, data in dict_score.items()}
            output_winner = {key: self.next_match_winner_plot(data) for key, data in dict_winner.items()}
            return self.merge_dicts(output_score, output_winner)
        else:
            return None















