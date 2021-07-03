from data.teams import team_game_map
from myapp.models import *
import numpy as np
from myproject.settings import AWS_S3_URL, DEFAULT_PHOTO
import pandas as pd
import requests
import environ
import os
from pathlib import Path
from data.teams import teams
import json
import data.viz_variables as vis
import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
from data.knockout import TEAM_GAME_MAP as TGM, CUP_GAMES, CUP_DRAW, CUP_DRAW_BETA
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY=str, )
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class UserCreds(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_profile(self):
        league_init = list(LeagueMember.objects.filter(user_name_id=self.user_id).values())
        leagues = [i['league_name_id'] for i in league_init] if league_init else None
        if leagues:
            league_members_init = list(LeagueMember.objects.filter(league_name_id__in=leagues).values())
        league_members = {}
        context = {
            'league_context': None,
            'league_users': {},
            'my_league_member_ids': None,
            'permissions': {
                'league': False,
                'league_member': False,
                'image': False,
                'bets': {
                    'groups': {'placed': False, 'id': None},
                    'top_16': {'placed': False, 'id': None},
                    'quarter_final': {'placed': False, 'id': None},
                    'semi_final': {'placed': False, 'id': None},
                    'final': {'placed': False, 'id': None},
                }
            },
            'views': {
                'extra_points': None,
                'cup': None
            },
        }
        if leagues:
            if sum([('Conference League' in item) or ('Beta Coffee' in item) for item in leagues]) > 0:
                context['views']['cup'] = True
            if league_members_init:
                for league in leagues:
                    context['permissions']['league'] = True
                    league_members[league] = [{
                        'uid': item['user_name_id'],
                        'member_id': item['id'],
                        'nick_name': item['nick_name'],
                        'full_name': f"{item['first_name']} {item['last_name']}"
                    } for item in league_members_init if item['league_name_id'] == league]
                all_user_ids = [i['uid'] for i in [j[0] for j in list(league_members.values())]]
                image_init = list(UserImage.objects.filter(user_name_id__in=all_user_ids).order_by('created').values())
                images = {i['user_name_id']: f"{AWS_S3_URL}{i['header_image']}" for i in image_init}
                default_image = f"{AWS_S3_URL}{DEFAULT_PHOTO}"
                for member in league_members.values():
                    for sub in member:
                        sub['image'] = default_image if sub['uid'] not in images.keys() else images[sub['uid']]
            my_league_member_ids = {}
            for key, val in league_members.items():
                for i in val:
                   if i['uid'] == self.user_id:
                       my_league_member_ids[key] = i['member_id']
            context['league_context'] = league_members
            context['my_league_member_ids'] = my_league_member_ids
            league_users = {}
            for key, val in league_members.items():
                league_users[key] = {i['uid']: i['nick_name'] for i in val}
            context['league_users'] = league_users
            if self.user_id in images.keys():
                context['permissions']['image'] = True
        G_G = list(Game.objects.filter(user_name_id=self.user_id).values('user_name_id', 'id'))
        if G_G:
            context['permissions']['bets']['groups']['placed'] = True
            context['permissions']['bets']['groups']['id'] = G_G[0]['id']
        G_16 = list(GameTop16.objects.filter(user_name_id=self.user_id).values('user_name_id', 'id'))
        if G_16:
            context['permissions']['bets']['top_16']['placed'] = True
            context['permissions']['bets']['top_16']['id'] = G_16[0]['id']
        G_8 = list(GameTop8.objects.filter(user_name_id=self.user_id).values('user_name_id', 'id'))
        if G_8:
            context['permissions']['bets']['quarter_final']['placed'] = True
            context['permissions']['bets']['quarter_final']['id'] = G_8[0]['id']
        G_4 = list(GameTop4.objects.filter(user_name_id=self.user_id).values('user_name_id', 'id'))
        if G_4:
            context['permissions']['bets']['semi_final']['placed'] = True
            context['permissions']['bets']['semi_final']['id'] = G_4[0]['id']
        G_2 = list(GameTop2.objects.filter(user_name_id=self.user_id).values('user_name_id', 'id'))
        if G_2:
            context['permissions']['bets']['final']['placed'] = True
            context['permissions']['bets']['final']['id'] = G_2[0]['id']
        print(context)
        return context


class RealScores(object):
    def __init__(self):
        self.TOKEN = 'bfa132288504de6860c8ae3259d21fa7'
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'
        self.L_API_PREFIX = f"http://livescore-api.com/api-client/"
        self.L_API_SUFFIX = f".json&competition_id=387&?key=KDbVwkzQSt1r7tCq&secret=ZS5RT5WXc7HyvUMgyXb4iLVaeWClqfMq"

    def all_matches_phase_1(self) -> list:
        data = requests.get(url=self.URL).json()
        output = []
        for item in data['calendar']['matchdays']:
            for subitem in item['matches']:
                row = {
                    'match_day_id': item['matchdayID'],
                    'match_round': item['matchdayName'],
                    'match_day_playoff': item['matchdayPlayoff'],
                    'match_day_type': item['matchdayType'],
                    'match_id': subitem['matchID'],
                    'match_status': subitem['matchStatus']['statusID'],
                    'match_date': subitem['matchDate'],
                    'match_hour': subitem['matchTime'],
                    'home_team': subitem['homeParticipant']['participantName'],
                    'home_team_id': subitem['homeParticipant']['participantID'],
                    'home_team_score': subitem['homeParticipant']['score'],
                    'away_team': subitem['awayParticipant']['participantName'],
                    'away_team_id': subitem['awayParticipant']['participantID'],
                    'away_team_score': subitem['awayParticipant']['score'],
                    'match_label': f"{subitem['homeParticipant']['participantName']}-{subitem['awayParticipant']['participantName']}"
                }
                output.append(row)
        return output

    def get_knockout_attributes(self, match_id):
        base_url = f"{self.PREFIX}/matches/{match_id}&apikey={self.TOKEN}"
        data = requests.get(url=base_url).json()
        score_90_min_home = int(data['match']['homeParticipant']['score']) - int(
            data['match']['extraTime']['home_score'])
        score_90_min_away = int(data['match']['awayParticipant']['score']) - int(
            data['match']['extraTime']['away_score'])
        extra_time = True if data['match']['extraTime']['is_extra'] == '1' else False
        penalties = False
        if 'stages' in data.keys():
            if data['stages']:
                stage_types = [i[1] for i in [list(item.values()) for item in data['stages']]]
                if 'Penalty Shootout' in stage_types:
                    loc = stage_types.index('Penalty Shootout')
                    if data['stages'][loc]['home_score'] is not None:
                        penalties = True
        if penalties:
            stage_score = data['stages'][loc]
            game_winner = data['match']['homeParticipant']['participantName'] if int(stage_score['home_score']) > int(stage_score['away_score']) \
                else data['match']['awayParticipant']['participantName'] if int(stage_score['home_score']) < int(stage_score['away_score']) else 'Draw'
        else:
            game_winner = data['match']['homeParticipant']['participantName'] if \
                int(data['match']['homeParticipant']['score']) > int(data['match']['awayParticipant']['score']) \
                else data['match']['awayParticipant']['participantName'] if \
                int(data['match']['homeParticipant']['score']) < int(data['match']['awayParticipant']['score']) else 'Draw'
        context = {
            'is_extra_time': extra_time,
            'home_score_90_min': score_90_min_home,
            'away_score_90_min': score_90_min_away,
            'home_score_end_match': data['match']['homeParticipant']['score'],
            'away_score_end_match': data['match']['awayParticipant']['score'],
            'match_winner': game_winner
        }
        return context

    def all_matches(self) -> list:
        data = self.all_matches_phase_1()
        for row in data:
            if row['match_day_playoff'] == '1':
                for key, val in self.get_knockout_attributes(row['match_id']).items():
                    row[key] = val
            else:
                row['is_extra_time'] = False
                row['home_score_90_min'] = row['home_team_score']
                row['away_score_90_min'] = row['away_team_score']
                row['home_score_end_match'] = row['home_team_score']
                row['away_score_end_match'] = row['away_team_score']
                row['match_winner'] = row['home_team'] if row['home_team_score'] > row['away_team_score']\
                                      else row['away_team'] if row['home_team_score'] < row['away_team_score'] \
                                      else 'Draw'
        for item in data:
            item['home_team_score'] = int(item['home_score_90_min']) if 'Final' in item['match_round'] else item['home_team_score']
            item['away_team_score'] = int(item['away_score_90_min']) if 'Final' in item['match_round'] else item['away_team_score']
            item['match_view_type'] = None
            item['match_started'] = 1 if item['match_status'] != '0' else 0
        routed_data = self.game_router(data)
        return routed_data

    def game_router(self, data: tuple):
        game_status = ['live' if i['match_status'] == '-1' else 'finished' if i['match_status'] == '1' else 'fixture'
                       for i in data]
        GS = Counter(game_status)
        games_played = 0
        if 'live' in GS.keys():
            games_played = GS['live'] + GS['finished']
            if GS['live'] > 1:
                mode = 'double_live'
                sub_data = [i for i in data if i['match_status'] == '-1'][:2]
                sub_data[0]['match_view_type'], sub_data[1]['match_view_type'] = 'next', 'prev'
            else:
                mode = 'live_and_legacy'
                sub_data_live = [i for i in data if i['match_status'] == '-1'][0:1]
                sub_data_legacy = [i for i in data if i['match_status'] == '1'][-1:]
                sub_data_live[0]['match_view_type'], sub_data_legacy[0]['match_view_type'] = 'next', 'prev'
        elif 'fixture' not in GS.keys():
            games_played = GS['finished']
            mode = 'double_legacy'
            sub_data = [i for i in data if i['match_status'] == '1'][-2:]
            sub_data[0]['match_view_type'], sub_data[1]['match_view_type'] = 'next', 'prev'
        else:
            games_played = GS['finished']
            mode = 'fixture_and_legacy'
            sub_data_fixture = [i for i in data if i['match_status'] == '0'][:1]
            sub_data_legacy = [i for i in data if i['match_status'] == '1'][-1:]
            sub_data_fixture[0]['match_view_type'], sub_data_legacy[0]['match_view_type'] = 'next', 'prev'
        return data, games_played

    @staticmethod
    def get_minimal_count_value(df) -> int:
        sorted_df = pd.DataFrame(df['event_count'].value_counts()).reset_index().sort_values(by='index', ascending=False)
        event_details = {item[0]: item[1] for item in sorted_df.values.tolist()}
        agg = 0
        for key, val in event_details.items():
            agg += val
            if agg >= 3:
                return int(key)

    def adjust_top_player_table(self, df):
        df_goal = df.loc[df.event_type == 'Top Scorer']
        df_assists = df.loc[df.event_type == 'Top Assist']
        adj_df_scorers = df_goal.loc[df_goal['event_count'] >= self.get_minimal_count_value(df_goal)]
        adj_df_df_assists = df_assists.loc[df_assists['event_count'] >= self.get_minimal_count_value(df_assists)]
        return pd.concat([adj_df_scorers, adj_df_df_assists])

    def top_players(self,) -> list:
        top_player_list_adjusted = []
        for item in [1, 2]:
            url = f'{self.PREFIX}/topplayers/40&apikey={self.TOKEN}&event_id={str(item)}&limit=1000'
            event_name = 'Top Scorer' if item == 1 else 'Top Assist'
            top_player_api = requests.get(url=url).json()['season']['players']
            top_player_list = [[item['shortname'], item['teamname'], int(item['eventCount']), f'{event_name}'] for item in top_player_api]
            for p in top_player_list:
                if [*p] == ['C. Ronaldo', 'Portugal', 2, 'Top Scorer']:
                    top_player_list_adjusted.append(['C. Ronaldo', 'Portugal', 5, 'Top Scorer'])
                else:
                    top_player_list_adjusted.append(p)
        df = pd.DataFrame(top_player_list_adjusted, columns=['name', 'team', 'event_count', 'event_type']).sort_values(by='event_count', ascending=False)
        df_adjusted = self.adjust_top_player_table(df)[['name', 'event_type']]
        df_adjusted['is_countable'] = True
        df_final = pd.merge(df, df_adjusted, on = ['name', 'event_type'], how = 'inner')
        return df_final.to_dict(orient='records')


class DataPrepHomePage(UserCreds):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.profile = self.get_user_profile()
        self.UserPred = UserPrediction(self.profile)
        self.df_games = RealScores().all_matches()
        self.player_stats = RealScores().top_players()
        self.player_selection = self.UserPred.top_players_selection()
        self.UserPoints = UserPoints(self.UserPred.prepare_user_prediction(), self.df_games, self.player_stats, self.player_selection)

    def show_league_tables(self):
        output = {}
        data = self.UserPoints.merged_data_games()
        for key, val in data.items():
            output[key] = self.UserPoints.build_league_table(val)
        return output

    def show_game_cards(self):
        if self.profile['permissions']['league']:
            df = list(self.UserPoints.merged_data_games().values())[0]
            data = df.loc[(df.user_name_id == self.user_id) &
                          (df.match_view_type.isin(['next', 'prev']))][
                                ['home_team', 'away_team', 'match_status', 'match_date', 'match_hour', 'home_score_90_min',
                                 'away_score_90_min', 'match_winner', 'predicted_score', 'pred_winner', 'match_view_type']
                                ].to_dict(orient="records")
            for item in data:
                item['home_logo'] = teams[item['home_team']]['logo']
                item['away_logo'] = teams[item['away_team']]['logo']
            if 'next' in list(df['match_view_type']) and 'prev' in list(df['match_view_type']):
                context = {
                    'next': [item for item in data if item['match_view_type'] == 'next'][0],
                    'prev': [item for item in data if item['match_view_type'] == 'prev'][0],
                    'games_played': int(df.loc[df.match_started == 1].shape[0]/len(set(list(df.user_name_id))))
                }
            else:
                context = {
                    'next': None,
                    'prev': None,
                    'games_played': int(df.loc[df.match_started == 1].shape[0] / len(set(list(df.user_name_id))))
                }
        else:
            context = {'next': None, 'prev': None, 'games_played': None}
        return context


class DataPrepShowPredictions(UserCreds):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.profile = self.get_user_profile()
        self.UserPred = UserPrediction(self.profile)
        self.df_games = RealScores().all_matches()
        self.player_stats = RealScores().top_players()
        self.player_selection = self.UserPred.top_players_selection()
        self.UserPoints = UserPoints(self.UserPred.prepare_user_prediction(), self.df_games, self.player_stats, self.player_selection)

    def present_all_predictions(self):
        output = {}
        data = self.UserPoints.merged_data_games()
        for key, val in data.items():
            output[key] = self.UserPoints.build_league_table(val)
        return output

    def present_player_selection(self):
        output = {}
        data = self.UserPoints.merged_data_games()
        for key, val in data.items():
            output[key] = self.UserPoints.build_league_table(val)
        return output


class UserPrediction:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    @staticmethod
    def group_stage_bets(ids: list):
        df = pd.DataFrame(list(Game.objects.filter(user_name_id__in=ids).values())).\
            drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id'). \
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('top_')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home', np.where(df.variable.str[-1:] == '1', 'Away', None))
        df['game_id'] = df.variable.str[4:-2]
        df['predicted_score'] = df['value'].astype(str)
        df_main = df.sort_values(by=['user_name_id', 'variable', 'location']).groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[[0, 1]]
        df_main['pred_winner'] = np.where(df_main['pred_score_home'] > df_main['pred_score_away'], 'home',
                                          np.where(df_main['pred_score_away'] > df_main['pred_score_home'],
                                          'away', 'draw'))
        return df_main

    @staticmethod
    def knockout_bets(df_init):
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('_alt')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home', np.where(df.variable.str[-1:] == '1', 'Away', None))
        df['game_id'] = df.variable.str[4:6]
        df['predicted_score'] = df['value'].astype(str)
        df_score = df[df.location.notnull()]
        df_winner = df[~df.location.notnull()][['user_name_id', 'game_id', 'value']]
        df_main = df_score.sort_values(by=['user_name_id', 'variable', 'location']).groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[[0, 1]]
        output = pd.merge(df_main, df_winner, on=['user_name_id', 'game_id'], how='inner').rename(columns={'value': 'pred_winner'})
        return output

    def prepare_user_prediction(self):
        leagues = self.user_profile['league_users']
        output = {}
        for key, ids_dict in leagues.items():
            ids = [i for i in ids_dict.keys()]
            df_main = self.group_stage_bets(ids)
            df_main['stage'] = 'group'
            df_init_top_16 = pd.DataFrame(list(GameTop16.objects.filter(user_name_id__in=ids).values()))
            if df_init_top_16.shape[0] > 0:
                df_top_16 = self.knockout_bets(df_init_top_16)
                df_top_16['stage'] = '1/8 Final'
                df_main = df_main.append(df_top_16)
                df_init_top_8 = pd.DataFrame(list(GameTop8.objects.filter(user_name_id__in=ids).values()))
                if df_init_top_8.shape[0] > 0:
                    df_top_8 = self.knockout_bets(df_init_top_8)
                    df_top_8['stage'] = '1/4 Final'
                    df_main = df_main.append(df_top_8)
                    df_init_top_4 = pd.DataFrame(list(GameTop4.objects.filter(user_name_id__in=ids).values()))
                    if df_init_top_4.shape[0] > 0:
                        df_top_4 = self.knockout_bets(df_init_top_4)
                        df_top_4['stage'] = '1/2 Final'
                        df_main = df_main.append(df_top_4)
                        df_init_top_2 = pd.DataFrame(list(GameTop2.objects.filter(user_name_id__in=ids).values()))
                        if df_init_top_2.shape[0] > 0:
                            df_top_2 = self.knockout_bets(df_init_top_4)
                            df_top_2['stage'] = 'Final'
                            df_main = df_main.append(df_top_2)
            nick_names = self.user_profile['league_users'][key]
            df_main['nickname'] = [nick_names[item] for item in list(df_main.user_name_id)]
            output[key] = df_main

        return output

    def top_players_selection(self) -> dict:
        output = {}
        for key, val in self.user_profile['league_users'].items():
            ids = [i for i in val.keys()]
            df_selection = pd.DataFrame(list(Game.objects.filter(user_name_id__in=ids).values())).\
                drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id'). \
                groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
            df = df_selection[df_selection.variable.str.contains('top_')]
            df['player_name'] = df.value.str.split(' - ', expand=True, n=1)[[1]]
            df['variable_type'] = [i[:-2] for i in list(df['variable'])]
            df['nickname'] = [val[i] for i in list(df['user_name_id'])]
            output[key] = df.to_dict(orient='records')
        return output


class UserPoints:
    def __init__(self, user_predictions: dict, real_results: dict, player_stats: dict = {}, player_selection: dict = {}):
        self.up = user_predictions
        self.rr = real_results[0]
        self.player_selection = player_selection
        self.player_stats = player_stats

    def merged_data_games(self) -> dict:
        output = {}
        df_games = pd.DataFrame(self.rr)
        df_games['rn'] = df_games.groupby('match_round').cumcount()
        df_games['alter_game_id'] = "a" + df_games['rn'].map(str)
        df_games['alter_game_id'] = "a" + df_games['rn'].map(str)
        df_groupstage = df_games.loc[df_games.match_day_playoff != '1']
        df_knockout = df_games.loc[df_games.match_day_playoff == '1']
        for key, val in self.up.items():
            df_groupstage_bets = val[val.stage == 'group']
            df_knockout_bets = val[val.stage != 'group']
            merged_groupstage = pd.merge(
                                    df_groupstage_bets,
                                    df_groupstage,
                                    left_on='game_id',
                                    right_on='match_id',
                                    how='inner')
            merged_knockout = pd.merge(
                                    df_knockout_bets,
                                    df_knockout,
                                    left_on=['game_id', 'stage'],
                                    right_on=['alter_game_id', 'match_round'],
                                    how='inner')
            df = pd.concat([merged_groupstage, merged_knockout])
            df['pred_winner'] = np.where(df.pred_winner == 'home',
                                         df.home_team,
                                         np.where(df.pred_winner == 'away',
                                                  df.away_team,
                                                  np.where(df.pred_winner == 'draw',
                                                           "Draw",
                                                           df.pred_winner)))
            df['is_boom'] = np.where((df.pred_score_home.astype(float) == df.home_score_90_min.astype(float)) &
                                     (df.pred_score_away.astype(float) == df.away_score_90_min.astype(float)), 1, 0)
            df['is_direction'] = np.where(df.pred_winner == df.match_winner, 1, 0)
            df['points'] = np.where(df.match_day_playoff == '1',
                                    np.where((df['is_boom'] == 1) & (df['is_direction'] == 1), 4,
                                             np.where((df['is_boom'] == 1) & (df['is_direction'] == 0), 3,
                                                      np.where(df['is_direction'] == 1, 1, 0))),
                                    np.where(df['is_boom'] == 1, 3, np.where(df['is_direction'] == 1, 1, 0)))
            df['distance'] = abs(df.home_score_90_min.astype(int) - df.pred_score_home.astype(int)) + \
                             abs(df.away_score_90_min.astype(int) - df.pred_score_away.astype(int))
            df['league_name'] = key
            output[key] = df
        return output

    def build_league_table(self, df):
        league_name = list(df.league_name)[0]
        required_cols = ['nickname', 'games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'distance', 'user_name_id']
        data = pd.DataFrame(df.groupby(['user_name_id', 'nickname']).apply(self.calc_league_table).reset_index())
        df = pd.DataFrame(self.adjust_table_column_type(data[required_cols]), columns=required_cols)
        player_selection_points = self.agg_points_from_players()[league_name]
        df['extra'] = [player_selection_points[i] for i in list(df.user_name_id)]
        df['points'] = df['extra'] + df['points']
        cleaner_data = df.sort_values(by=['points', 'boom', 'direction', 'predicted_goals', 'distance'], ascending=[False] * 4 + [True])
        cleaner_data['rn'] = np.arange(len(cleaner_data)) + 1
        return cleaner_data.to_dict(orient='records')

    @staticmethod
    def calc_league_table(x):
        d = [
            x['match_started'].sum(),
            (x['match_started'] * x['points']).sum(),
            (x['match_started'] * x['is_boom']).sum(),
            (x['match_started'] * x['is_direction']).sum(),
            round((x['match_started'] * x['points']).sum() * 100 / ((x['match_started'] * 3)).sum(), 1),
            (x['match_started'] * x['is_boom'] * (
             x['pred_score_home'].astype(int) + x['pred_score_away'].astype(int))).sum(),
            (x['match_started'] * x['distance']).sum(),
        ]
        index_names = ['games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'distance']
        return pd.Series(d, index=[index_names])

    @staticmethod
    def adjust_table_column_type(data) -> list:
        adj_df = []
        for item in data.values.tolist():
            nick = [item[0]]
            values1 = [int(sub) for sub in item[1:5]]
            values2 = [int(sub) for sub in item[6:]]
            adj_df.append(nick + values1 + [f"{item[5]}%"] + values2)
        return adj_df

    def merged_data_players(self, excluded_league: list = [24, 19, 31]) -> dict:
        user_selection = self.player_selection
        df_players = pd.DataFrame(self.player_stats).rename(columns={'name': 'player_name'})
        output = {}
        excluded_league_names = [i['league_name'] for i in list(League.objects.filter(id__in=excluded_league).values('league_name'))]
        for key, val in user_selection.items():
            df_users = pd.DataFrame(val).rename(columns={'variable_type': 'event_type'})
            unique_users = list(df_users.user_name_id.unique())
            df_users['event_type'] = np.where(df_users['event_type'] == 'top_scorer', 'Top Scorer',
                                              np.where(df_users['event_type'] == 'top_assist',
                                                       'Top Assist', None))
            new_cols = ['user_name_id', 'nickname', 'event_type', 'player_name', 'team', 'event_count']
            df_merged = pd.merge(df_users, df_players, on=['player_name', 'event_type'], how='inner')[new_cols]
            if key in excluded_league_names:
                output[key] = {'data': df_merged, 'points': {i: 0 for i in unique_users}}
            else:
                df_output = df_merged.groupby(['user_name_id', 'nickname', 'event_type', 'player_name']).first().reset_index()
                listed_user_players = list(df_output['user_name_id'].values)
                user_points = {item: listed_user_players.count(item) * 3 if item in list(set(listed_user_players)) else 0
                               for item in unique_users}
                output[key] = {'data': df_merged, 'points': user_points}
        return output

    def agg_points_from_players(self):
        data = self.merged_data_players()
        points = {}
        for key, val in data.items():
            points[key] = val['points']
        return points


class PlotBuilder(UserCreds):
    def __init__(self, user_id, match_type='prev'):
        super().__init__(user_id)
        self.profile = self.get_user_profile()
        self.UserPred = UserPrediction(self.profile)
        self.df_games = RealScores().all_matches()
        self.player_stats = RealScores().top_players()
        self.player_selection = self.UserPred.top_players_selection()
        self.UserPoints = UserPoints(self.UserPred.prepare_user_prediction(), self.df_games, self.player_stats, self.player_selection)
        self.match_type = match_type
        self.game_meta = None
        self.user_titles = {}

    def match_prediction_df(self):
        input_data = self.UserPoints.merged_data_games()
        output = {}
        if input_data is not None:
            df_meta = list(input_data.values())[0]
            self.game_meta = df_meta.loc[df_meta.match_view_type == self.match_type].to_dict(orient='records')[0]
            for key, val in input_data.items():
                df = pd.DataFrame(val)
                df = df.loc[df.match_view_type == self.match_type]
                df['predicted_score_alternative'] = np.where(df['pred_winner'] == df.away_team,
                                                             df['pred_score_away'] + '-' + df['pred_score_home'],
                                                             df['predicted_score'])
                df_scores = pd.DataFrame(
                    df.groupby(['predicted_score_alternative', 'pred_winner'])['match_status'].count()).reset_index(). \
                    rename(columns={
                            'match_status': 'count',
                            'predicted_score_alternative': 'score',
                            'pred_winner': 'winner'
                    }).merge(vis.SCORE_MAP_DF, on='score', how='inner')
                df_fig = df_scores.sort_values(by=['score_rank', 'winner'])
                output[key] = df_fig
            return output
        else:
            return None

    def match_winner_df(self):
        input_data = self.UserPoints.merged_data_games()
        output = {}
        if input_data is not None:
            for key, val in input_data.items():
                df = pd.DataFrame(val)
                df = df[df.match_view_type == self.match_type]
                df_winner = pd.DataFrame(df.groupby(['pred_winner'])['match_status'].count()). \
                    reset_index().rename(columns={
                                    'match_status': 'count',
                                    'pred_winner': 'winner'
                                  })
                output[key] = df_winner
            return output
        else:
            return None

    @staticmethod
    def match_prediction_plot(data):
        fig = px.bar(
            data,
            x='score', y='count', color="winner", template='simple_white', text='count',
            title="Score Distribution", labels={"score": "Score", "count": "Prediction Count", "winner": ""})
        fig.update_traces(textposition='inside')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def match_winner_plot(data):
        fig = px.pie(data, values='count', names='winner', title='Predicted Winner')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def merge_dicts(a: dict, b: dict):
        new_output = {}
        for i, j in zip(a.items(), b.items()):
            if i[0] == j[0]:
                new_output[i[0]] = [i[1], j[1]]
        return new_output

    def main(self):
        dict_score = self.match_prediction_df()
        dict_winner = self.match_winner_df()
        if dict_score is not None:
            output_score = {key: self.match_prediction_plot(data) for key, data in dict_score.items()}
            output_winner = {key: self.match_winner_plot(data) for key, data in dict_winner.items()}
            return self.merge_dicts(output_score, output_winner)
        else:
            return None

    @staticmethod
    def build_sankey_plot(data: dict) -> dict:
        link = dict(source=data['source'], target=data['target'], value=data['value'])
        node = dict(label=data['label'], pad=40, thickness=5)
        plot_data = go.Sankey(link=link, node=node)
        fig = go.Figure(plot_data)
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def unique(list1):
        unique_list = []
        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    @staticmethod
    def ranked_items(x):
        seq = sorted(x)
        index = [seq.index(v) for v in x]
        return index

    @staticmethod
    def score_distance(score_list: list) -> int:
        if score_list[2] > score_list[0] or score_list[3] > score_list[1]:
            return 15
        else:
            home_distance = score_list[0] - score_list[2]
            away_distance = score_list[1] - score_list[3]
            return home_distance + away_distance

    def data_sankey_live_game(self, data) -> dict:
        predicted_result = [j['predicted_score'] for j in data]
        user_ids = [j['user_name_id'] for j in data]
        user_rank = [j['league_rank'] for j in data]
        unique_user_ids = self.unique(user_ids)
        ranked_unique_user_ids = self.ranked_items(unique_user_ids)
        source_map = {key: val for key, val in zip(unique_user_ids, ranked_unique_user_ids)}
        source = [source_map[i] for i in user_ids]
        users = [obj['nickname'] for obj in data]
        unique_users_pre = self.unique(users)
        unique_users = [f"{i} ({r})" for i, r in zip(unique_users_pre, user_rank)]
        unique_results = self.unique(predicted_result)
        label = unique_users + unique_results
        n_start, n_results = len(ranked_unique_user_ids), len(unique_results)
        n_end = n_results + n_start + 1
        result_id = {obj: key for key, obj in zip(range(n_start, n_end), unique_results)}
        target = [result_id[obj['predicted_score']] for obj in data]
        value = [1 / (0.1 if item['distance'] == 0 else item['distance']) for item in data]
        return {'source': source, 'target': target, 'value': value, 'label': label}

    def live_winners(self, data: dict, league_name: str) -> dict:
        df = pd.DataFrame(data)[['user_name_id', 'nickname', 'pred_score_home', 'pred_score_away', 'home_score_90_min',
                                 'away_score_90_min', 'pred_winner', 'match_winner']].\
            rename(columns={
                     'nickname': 'nick',
                     'pred_score_home': 'p_h',
                     'pred_score_away': 'p_a',
                     'home_score_90_min': 'r_h',
                     'away_score_90_min': 'r_a',
                     'match_winner': 'real_winner'})
        df['user_type'] = np.where(((df.p_h == df.r_h) & (df.p_a == df.r_a)),
                                   'boomer',
                                   np.where(df.pred_winner == df.real_winner, 'winner', 'Loser'))
        relevant_users = [i for i in list(df[df.user_type != 'Loser']['user_name_id'].unique())]
        images = {j['uid']: j['image'] for j in self.profile['league_context'][league_name] if
                  j['uid'] in relevant_users}
        output = {
            'Boomers': [[r['nickname'], r['user_name_id'], images[r['user_name_id']]] for r in df[df.user_type == 'boomer'].to_dict(orient='records')],
            'Winners': [[r['nickname'], r['user_name_id'], images[r['user_name_id']]] for r in df[df.user_type == 'winner'].to_dict(orient='records')],
        }
        return output

    def live_game_plot(self) -> dict:
        output = {}
        input_data = self.UserPoints.merged_data_games()
        if input_data is not None:
            df_meta = list(input_data.values())[0]
            self.game_meta = df_meta.loc[df_meta.match_view_type == self.match_type].to_dict(orient='records')[0]
            for key, df in input_data.items():
                league_table = self.UserPoints.build_league_table(df)
                this_game_df = df.loc[df.match_view_type == self.match_type]
                self.user_titles[key] = self.live_winners(this_game_df.to_dict(orient='records'), league_name=key)
                league_rank = {i['user_name_id']: i['rn'] for i in league_table}
                game_data = this_game_df.to_dict(orient='records')
                init_data = [{
                        'user_name_id': j['user_name_id'],
                        'nickname': j['nickname'],
                        'predicted_score': j['predicted_score'],
                        'distance': self.score_distance([
                                int(j['pred_score_home']),
                                int(j['pred_score_away']),
                                int(j['home_score_90_min']),
                                int(j['away_score_90_min'])
                            ]),
                        'league_rank': league_rank[j['user_name_id']]
                    } for j in game_data]
                relevant_data = [item for item in init_data if item['distance'] < 15]
                data_preps = self.data_sankey_live_game(relevant_data)
                output[key] = self.build_sankey_plot(data_preps)
        return output


class UserPredictionBase:
    def __init__(self, user_id):
        self.TOKEN = env('API_TOKEN')
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'
        self.user_id = user_id

    def extract_data(self):
        return requests.get(url=self.URL).json()

    def get_api_data(self) -> dict:
        metadata = {}
        for item in self.extract_data()['calendar']['matchdays']:
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
                    'away_team': away_team,
                    'real_score_home_90_min': real_score_home,
                    'real_score_away_90_min': real_score_away,
                    'score_label_90_min': real_score_away,
                }
        return metadata

    def get_user_leagues(self) -> tuple:
        league_member_data = list(LeagueMember.objects.filter(user_name_id=self.user_id).values())
        leagues = [item['league_name_id'] for item in league_member_data]
        if len(leagues) > 0:
            return True, leagues
        else:
            return False, None

    def is_cup_user(self) -> tuple:
        leagues = list(LeagueMember.objects.filter(user_name_id=self.user_id).values('league_name_id'))
        if len(leagues) > 0:
            league_list = [item['league_name_id'] for item in leagues]
            output = True if sum([('Conference League' in item) or
                                  ('Beta Coffee' in item) for item in league_list]) > 0 else False
            return output
        else:
            return None

    def get_league_members(self):
        leagues = self.get_user_leagues()
        if leagues[0]:
            league_data_output = []
            for obj in leagues[1]:
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

    def get_league_members_data(self) -> dict:
        data = LeagueMember.objects.filter(user_name_id=self.user_id)
        if len(data) > 0:
            league_data = list(data.values())
            output = {}
            for item in league_data:
                output[item['league_name_id']] = item['id']
            return output
        else:
            return None

    def user_game_bet_id(self, stage) -> dict:
        if stage == 'group':
            data = Game.objects.filter(user_name_id=self.user_id)
        if stage == 'top_16':
            data = GameTop16.objects.filter(user_name_id=self.user_id)
        if stage == 'top_8':
            data = GameTop8.objects.filter(user_name_id=self.user_id)
        if stage == 'top_4':
            data = GameTop4.objects.filter(user_name_id=self.user_id)
        if stage == 'top_2':
            data = GameTop2.objects.filter(user_name_id=self.user_id)
        if len(data) > 0:
            return data[0].id
        else:
            return None

    def extract_relevant_user_ids(self) -> list:
        leagues = list(LeagueMember.objects.filter(user_name_id=self.user_id).values('league_name'))
        ids = list(
            LeagueMember.objects.filter(league_name_id__in=[i['league_name'] for i in leagues]).values('user_name_id'))
        return [i['user_name_id'] for i in ids]

    @staticmethod
    def extract_group_stage_predictions(ids: list):
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id__in=ids).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id'). \
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('top_')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home',
                                  np.where(df.variable.str[-1:] == '1', 'Away', None))
        df['game_id'] = df.variable.str[4:-2]
        df['predicted_score'] = df['value'].astype(str)
        df_main = df.sort_values(by=['user_name_id', 'variable', 'location']).groupby(['user_name_id', 'game_id'])[
            'predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[
            [0, 1]]
        df_main['pred_winner'] = None
        return df_main

    @staticmethod
    def extract_knockout_predictions(df_init):
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id'). \
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('_alt')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home',
                                  np.where(df.variable.str[-1:] == '1', 'Away', None))
        df['game_id'] = df.variable.str[4:6]
        df['predicted_score'] = df['value'].astype(str)
        df_score = df[df.location.notnull()]
        df_winner = df[~df.location.notnull()][['user_name_id', 'game_id', 'value']]
        df_main = df_score.sort_values(by=['user_name_id', 'variable', 'location']). \
            groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[
            [0, 1]]
        output = pd.merge(df_main, df_winner, on=['user_name_id', 'game_id'], how='inner').rename(
            columns={'value': 'pred_winner'})
        return output

    def get_user_prediction(self):
        relevant_ids = self.extract_relevant_user_ids()
        df_main = self.extract_group_stage_predictions(relevant_ids)
        df_main['stage'] = 'group'
        df_init_top_16 = pd.DataFrame(list(GameTop16.objects.filter(user_name_id__in=relevant_ids).values()))
        if df_init_top_16.shape[0] > 0:
            df_top_16 = self.extract_knockout_predictions(df_init_top_16)
            df_top_16['stage'] = 'top_16'
            df_main = df_main.append(df_top_16)
            df_init_top_8 = pd.DataFrame(list(GameTop8.objects.filter(user_name_id__in=relevant_ids).values()))
            if df_init_top_8.shape[0] > 0:
                df_top_8 = self.extract_knockout_predictions(df_init_top_8)
                df_top_8['stage'] = 'top_8'
                df_main = df_main.append(df_top_8)
                df_init_top_4 = pd.DataFrame(list(GameTop4.objects.filter(user_name_id__in=relevant_ids).values()))
                if df_init_top_4.shape[0] > 0:
                    df_top_4 = self.extract_knockout_predictions(df_init_top_4)
                    df_top_4['stage'] = 'top_4'
                    df_main = df_main.append(df_top_4)
                    df_init_top_2 = pd.DataFrame(list(GameTop2.objects.filter(user_name_id__in=relevant_ids).values()))
                    if df_init_top_2.shape[0] > 0:
                        df_top_2 = self.extract_knockout_predictions(df_init_top_4)
                        df_top_2['stage'] = 'top_2'
                        df_main = df_main.append(df_top_2)
        return df_main

    def fetch_user_league_membership_data(self, user_id):
        relevant_ids = self.extract_relevant_user_ids()
        league_member_fields = ['user_name_id', 'first_name', 'last_name', 'league_name_id', 'nick_name', 'created']
        df_league_member_pre = pd.DataFrame(list(LeagueMember.objects.filter(user_name_id__in=relevant_ids).values()))[
            league_member_fields]. \
            sort_values(by=['user_name_id', 'league_name_id', 'created'], ascending=[True, True, False])
        leagues = list(df_league_member_pre[df_league_member_pre.user_name_id == user_id].league_name_id.unique())
        df_league_member = df_league_member_pre.groupby(['user_name_id', 'league_name_id']).first(). \
            reset_index().drop(columns='created')
        return df_league_member[df_league_member.league_name_id.isin(leagues)]

    def get_top_players_predictions(self) -> dict:
        relevant_ids = self.extract_relevant_user_ids()
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id__in=relevant_ids).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id'). \
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[df.variable.str.contains('top_')]
        df['player_name'] = df.value.str.split(' - ', expand=True, n=1)[[1]]
        df['variable_type'] = df.variable.str[:-2]
        df_predictions = df[['user_name_id', 'variable_type', 'player_name', 'value']]
        df_league = self.fetch_user_league_membership_data(self.user_id)[
            ['user_name_id', 'nick_name', 'league_name_id']]
        output_df = pd.merge(df_predictions, df_league, on='user_name_id', how='inner')
        leagues = list(output_df.league_name_id.unique())
        output = {league: output_df[output_df.league_name_id == league].values.tolist() for league in leagues}
        return output

    def get_top_players_my_predictions(self) -> dict:
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id=self.user_id).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id'). \
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[df.variable.str.contains('top_')]
        df['player_name'] = df.value.str.split(' - ', expand=True, n=1)[[1]]
        df['event_type'] = df.variable.str[:-2]
        df_predictions = df[['user_name_id', 'event_type', 'player_name', 'value']]
        df_predictions['event_type'] = np.where(df_predictions['event_type'] == 'top_scorer', 'Top Scorer',
                                                'Top Assist')
        df_real_players = TopPlayerStats(self.user_id).top_players_real()
        df_output = pd.merge(df_predictions, df_real_players[1], on=['player_name', 'event_type'], how='left')
        output = {item: df_output[df_output.event_type == item][['player_name', 'team', 'count']].values.tolist()
                  for item in ['Top Scorer', 'Top Assist']}
        return output

    def merge_predictions_with_api(self):
        extra_fields = ['game_id', 'match_label', 'real_score', 'real_score_home', 'real_score_away',
                        'game_status', 'date', 'hour', 'is_playoff', 'match_type', 'home_team', 'away_team',
                        'knockout_winner']
        metadata = self.get_api_data()
        df_user_predictions = self.get_user_prediction()
        data_enrichment = [
            [key,
             val['match_label'],
             val['score_label'],
             val['real_score_home'],
             val['real_score_away'],
             val['status'],
             val['date'],
             val['time'],
             val['is_playoff'],
             val['match_type'],
             val['home_team'],
             val['away_team'],
             None if val['is_playoff'] != '1' else val['home_team'] if val['real_score_home'] > val[
                 'real_score_away'] else val['away_team']
             ] for key, val in metadata.items()]

        df_enrichment = pd.DataFrame(data_enrichment, columns=extra_fields)
        df_enrichment['rn'] = df_enrichment.groupby('match_type').cumcount()
        df_enrichment['alter_game_id'] = "a" + df_enrichment['rn'].map(str)
        df_enrichment_groupstage = df_enrichment[df_enrichment.is_playoff != '1']
        df_enrichment_knockout = df_enrichment[df_enrichment.is_playoff == '1']

        knockout_features = ['is_extra_time', 'home_score_90_min', 'away_score_90_min', 'home_score_end_match',
                             'away_score_end_match', 'match_winner']
        adjusted_features = list(df_enrichment_groupstage.columns) + knockout_features

        df_enrichment_knockout_init = []
        for item in df_enrichment_knockout.values.tolist():
            item += [*GetMatchData().get_knockout_attributes(item[0]).values()]
            df_enrichment_knockout_init.append(item)

        df_enrichment_knockout = pd.DataFrame(df_enrichment_knockout_init, columns=adjusted_features)

        for col in knockout_features:
            df_enrichment_groupstage[col] = None

        df_user_predictions_groupstage = df_user_predictions[df_user_predictions.stage == 'group']
        df_user_predictions_knockout = df_user_predictions[df_user_predictions.stage != 'group']
        df_user_predictions_knockout['stage'] = np.where(df_user_predictions_knockout['stage'] == 'top_16',
                                                         '1/8 Final',
                                                         np.where(df_user_predictions_knockout['stage'] == 'top_8',
                                                                  '1/4 Final',
                                                                  np.where(
                                                                      df_user_predictions_knockout['stage'] == 'top_4',
                                                                      '1/2 Final', 'Final')))

        df_groupstage_final = pd.merge(df_user_predictions_groupstage, df_enrichment_groupstage, on=['game_id'],
                                       how='inner')
        df_knockout_final = pd.merge(
            df_user_predictions_knockout,
            df_enrichment_knockout,
            left_on=['game_id', 'stage'],
            right_on=['alter_game_id', 'match_type'],
            how='inner').drop(columns=['rn', 'alter_game_id'])

        df_final = pd.concat([df_groupstage_final, df_knockout_final])

        user_level_fields = ['user_name_id', 'first_name', 'last_name', 'league_name_id', 'nick_name', 'created']
        df_user_level_pre = pd.DataFrame(
            list(LeagueMember.objects.filter(user_name_id__in=self.extract_relevant_user_ids()).
                 values()))[user_level_fields].sort_values(
            by=['user_name_id', 'league_name_id', 'created'],
            ascending=[True, True, False])
        df_user_level = df_user_level_pre.groupby(['user_name_id', 'league_name_id']).first(). \
            reset_index().drop(columns='created')

        output = pd.merge(df_final, df_user_level, on=['user_name_id'], how='inner').sort_values(
            by=['date', 'hour', 'user_name_id'])
        output['user_full_name'] = output['first_name'] + ' ' + output['last_name']
        output['date'] = output['date'].str[5:]

        output_fields = [
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
            'real_score_away',
            'is_playoff',
            'match_type',
            'home_team',
            'away_team',
            'pred_winner',
            'is_extra_time',
            'home_score_90_min',
            'away_score_90_min',
            'home_score_end_match',
            'away_score_end_match',
            'match_winner',
        ]
        df_output = output[output_fields].rename(columns={'match_winner': 'knockout_winner'})
        return df_output

    def present_predictions(self) -> tuple:
        data = self.merge_predictions_with_api()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        if len(leagues) > 0:
            output = {}
            required_fields = ['nick_name', 'date', 'hour', 'match_label', 'predicted_score', 'real_score',
                               'game_status', 'pred_score_home', 'pred_score_away', 'real_score_home',
                               'real_score_away', 'user_name_id', 'match_type', 'is_playoff', 'pred_winner',
                               'knockout_winner', 'is_extra_time', 'home_score_90_min', 'away_score_90_min',
                               'home_score_end_match', 'away_score_end_match']
            for item in leagues:
                filtered_df = data[(data.league_name_id == item)][required_fields]
                filtered_df['status_rank'] = np.where(filtered_df.game_status == 'Finished', 1, 0)
                final_df = filtered_df.sort_values(by=['status_rank', 'date', 'hour']).drop(columns='status_rank')
                output[item] = final_df.values.tolist()
            return output, required_fields
        else:
            return None, None, None

    def present_my_predictions(self):
        data = self.merge_predictions_with_api()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        if len(leagues) > 0:
            output = {}
            required_fields = ['nick_name', 'date', 'hour', 'match_label', 'predicted_score', 'real_score',
                               'game_status', 'pred_score_home', 'pred_score_away', 'real_score_home',
                               'real_score_away', 'user_name_id', 'match_type', 'is_playoff', 'pred_winner',
                               'knockout_winner', 'is_extra_time', 'home_score_90_min', 'away_score_90_min',
                               'home_score_end_match', 'away_score_end_match']
            for item in leagues:
                filtered_df = data[(data.league_name_id == item) & (data.user_name_id == self.user_id)][required_fields]
                filtered_df['status_rank'] = np.where(filtered_df.game_status == 'Finished', 1, 0)
                final_df = filtered_df.sort_values(by=['status_rank', 'date', 'hour']).drop(columns='status_rank')
                output[item] = final_df.values.tolist()
            return output[leagues[0]], required_fields
        else:
            return None, None

    @staticmethod
    def add_game_attributes(data, item, game_label):
        x = data[(data.league_name_id == item) & (data.match_label == game_label)]
        x['pred_dir'] = np.where(x.pred_score_home > x.pred_score_away, 'home',
                                 np.where(x.pred_score_home < x.pred_score_away, 'away', 'draw'))
        x['real_dir'] = np.where(x.real_score_home > x.real_score_away,
                                 'home', np.where(x.real_score_home < x.real_score_away, 'away', 'draw'))
        x['is_direction'] = np.where(x.is_playoff != '1',
                                     np.where(x.pred_dir == x.real_dir, 1, 0),
                                     np.where(x.pred_winner == x.knockout_winner, 1, 0))
        x['is_boom'] = np.where((x.pred_score_home == x.real_score_home) & (x.pred_score_away == x.real_score_away), 1,
                                0)
        return x

    def user_game_points(self, matches: list = []):
        data = self.merge_predictions_with_api()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        api_game_router = GetMatchData().game_router()
        next_game = api_game_router['next']['data']
        prev_game = api_game_router['prev']['data']
        if len(leagues) > 0:
            output = {}
            for item in leagues:
                x = {
                    'next': self.add_game_attributes(data, item, next_game['match_label']),
                    'prev': self.add_game_attributes(data, item, prev_game['match_label'])
                }
                boomers = {key: list(val[val.is_boom == 1].nick_name) for key, val in x.items()}
                winners = {key: list(np.setdiff1d(list(val[val.is_direction == 1].nick_name), boomers[key])) for
                           key, val in x.items()}
                user_pred_df_next = x['next'].loc[x['next'].user_name_id == self.user_id]
                user_pred_df_prev = x['prev'].loc[x['prev'].user_name_id == self.user_id]
                if user_pred_df_prev.shape[0] > 0 and user_pred_df_next.shape[0] > 0:
                    user_nick = user_pred_df_next.nick_name.values[0]
                    user_pred = {
                        'next': user_pred_df_next.predicted_score.values[0],
                        'next_winner': user_pred_df_next.pred_winner.values[0],
                        'prev': user_pred_df_prev.predicted_score.values[0],
                        'prev_winner': user_pred_df_prev.pred_winner.values[0]
                    }
                    user_score = {key: 'Boom' if user_nick in value else '' for key, value in boomers.items()}
                    output[item] = {'boom': boomers, 'winner': winners, 'user_pred': user_pred,
                                    'user_score': user_score}
                else:
                    output[item] = {'boom': None, 'winner': None, 'user_pred': None, 'user_score': None}
            if user_pred_df_prev.shape[0] > 0 and user_pred_df_next.shape[0] > 0:
                reshaped_output = {key: {
                    'next': {
                        'boom': value['boom']['next'],
                        'winner': value['winner']['next'],
                        'user_pred': value['user_pred']['next'],
                        'user_score': value['user_score']['next'],
                        'user_pred_winner': value['user_pred']['next_winner']
                    },
                    'prev': {
                        'boom': value['boom']['prev'],
                        'winner': value['winner']['prev'],
                        'user_pred': value['user_pred']['prev'],
                        'user_score': value['user_score']['prev'],
                        'user_pred_winner': value['user_pred']['prev_winner']
                    }
                } for key, value in output.items()}
                return reshaped_output

            else:
                return None
        else:
            return None

    def home_screen_match_relevant_data(self, data):
        next_match = data['next']['data']
        prev_match = data['prev']['data']
        user_data = self.user_game_points(matches=[next_match['match_label'], prev_match['match_label']])
        if isinstance(user_data, dict):
            some_league = list(user_data.keys())[0]
            next_match['user_pred'] = user_data[some_league]['next']['user_pred']
            next_match['user_pred_winner'] = user_data[some_league]['next']['user_pred_winner']
            prev_match['user_pred'] = user_data[some_league]['prev']['user_pred']
            prev_match['user_pred_winner'] = user_data[some_league]['prev']['user_pred_winner']
            return prev_match, next_match, user_data
        else:
            return None, None, None

    @staticmethod
    def league_table(x):
        x['pred_dir'] = np.where(x.pred_score_home > x.pred_score_away,
                                 'home',
                                 np.where(x.pred_score_home < x.pred_score_away,
                                          'away',
                                          'draw'))
        x['real_dir'] = np.where(x.real_score_home > x.real_score_away,
                                 'home', np.where(x.real_score_home < x.real_score_away,
                                                  'away',
                                                  'draw'))
        x['is_direction'] = np.where((x.is_playoff != '1') &
                                     (x.pred_dir == x.real_dir), 1, 0)

        x['is_boom'] = np.where((x.is_playoff != '1') &
                                (x.pred_score_home == x.real_score_home) &
                                (x.pred_score_away == x.real_score_away), 1, 0)

        x['is_knockout_boom'] = np.where((x.is_playoff == '1') &
                                         (x.pred_score_home.astype(int) == x.home_score_90_min) &
                                         (x.pred_score_away.astype(int) == x.away_score_90_min), 1, 0)

        x[['home_team', 'away_team']] = x.match_label.str.split('-', n=2, expand=True)

        x['knockout_winner'] = np.where(x['knockout_winner'] == 'home',
                                        x['home_team'],
                                        np.where(x['knockout_winner'] == 'away',
                                                 x['away_team'],
                                                 x['knockout_winner']))

        x['is_knockout_direction'] = np.where((x.is_playoff == '1') & (x.pred_winner == x.knockout_winner), 1, 0)

        x['knockout_points'] = np.where((x.is_knockout_direction == 1) & (x.is_knockout_boom == 1),
                                        4,
                                        np.where((x.is_knockout_direction != 1) & (x.is_knockout_boom == 1),
                                                 3,
                                                 np.where((x.is_knockout_direction == 1) & (x.is_knockout_boom != 1),
                                                          1,
                                                          0)))

        x['points'] = np.where(x.is_playoff != '1',
                               np.where(x.is_boom == 1,
                                        3,
                                        np.where(x.is_direction == 1,
                                                 1,
                                                 0)),
                               x['knockout_points'])

        x['started'] = np.where(x.game_status != 'Fixture', 1, 0)
        x['is_live'] = np.where(x.game_status == 'live', 1, 0)
        x['distance'] = np.where(x.is_playoff != '1',
                                 (abs(x.real_score_home.astype(int) - x.pred_score_home.astype(int))) + (
                                     abs(x.real_score_away.astype(int) - x.pred_score_away.astype(int))),
                                 (abs(x.home_score_90_min - x.pred_score_home.astype(int))) + (
                                     abs(x.away_score_90_min - x.pred_score_away.astype(int))))

        d = [
            int(x['started'].sum()),  # started games
            int((x['started'] * x['points']).sum()),  # total points
            int(((x['started'] * x['is_boom']) + (x['started'] * x['is_knockout_boom'])).sum()),  # total booms
            int(((x['started'] * x['is_direction']) + (x['started'] * x['is_knockout_direction'])).sum()),
            # total directions
            round((x['started'] * x['points']).sum() * 100 / ((x['started'] * 3)).sum(), 1),  # success rate
            int((x['started'] * (x['is_boom'] + x['is_knockout_boom']) * (
                        x['pred_score_home'].astype(int) + x['pred_score_away'].astype(int))).sum()),  # B-goals
            int((x['is_live'] * x['points']).sum()),  # live points
            int(1),
            int((x['started'] * x['distance']).sum())  # total distance
        ]
        index_names = ['games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'live_points',
                       'players', 'distance']
        return pd.Series(d, index=[index_names])

    @staticmethod
    def adjust_table_column_type(data) -> list:
        adj_df = []
        for item in data.values.tolist():
            nick = [item[0]]
            values1 = [int(sub) for sub in item[1:5]]
            values2 = [int(sub) for sub in item[6:]]
            adj_df.append(nick + values1 + [f"{item[5]}%"] + values2)
        return adj_df

    @staticmethod
    def adjust_cup_table_column_type(data) -> list:
        adj_df = []
        for item in data.values.tolist():
            nick = [item[0]]
            values1 = [int(sub) for sub in item[1:5]]
            values2 = [int(sub) for sub in item[6:]]
            adj_df.append(nick + values1 + [f"{item[5]}%"] + values2)
        return adj_df

    def league_member_points(self):
        metadata = self.present_predictions()
        output = {}
        points_from_players = self.get_game_points_players()
        if metadata[0] is not None:
            for key, obj in metadata[0].items():
                df = pd.DataFrame(obj, columns=metadata[1])
                output[key] = self.get_game_points_group_stage(df, points_from_players[key])
            return output
        else:
            return None, None

    def league_member_points_cup(self, stage: str = None):
        metadata = self.present_predictions()
        output = {}
        if metadata[0] is not None:
            for key, obj in metadata[0].items():
                df = pd.DataFrame(obj, columns=metadata[1])
                df = df[df.match_label.isin(CUP_GAMES[stage])]
                if df.shape[0] > 0:
                    output[key] = self.get_game_points_cup(df)
                else:
                    output[key] = None
            return output
        else:
            return None

    def get_game_points_group_stage(self, df, player_points: dict):
        required_cols = ['nick_name', 'games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals',
                         'live_points', 'distance', 'user_name_id']
        data = pd.DataFrame(df.groupby(['user_name_id', 'nick_name']).apply(self.league_table).reset_index())
        df = pd.DataFrame(self.adjust_table_column_type(data[required_cols]), columns=required_cols)
        df['player_point_col'] = [int(player_points[item[1]]) for item in data.values.tolist()]
        df['points'] = df['player_point_col'] + df['points']
        cleaner_data = df.sort_values(by=['points', 'boom', 'direction', 'predicted_goals', 'distance'],
                                      ascending=[False] * 4 + [True])
        cleaner_data['rn'] = np.arange(len(cleaner_data)) + 1
        return cleaner_data.values.tolist()

    def get_game_points_cup(self, df):
        required_cols = ['nick_name', 'games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals',
                         'live_points', 'distance', 'user_name_id']
        data = pd.DataFrame(df.groupby(['user_name_id', 'nick_name']).apply(self.league_table).reset_index())
        cleaner_data = data.sort_values(
            by=[('points',), ('boom',), ('direction',), ('predicted_goals',), ('distance',)],
            ascending=[False] * 4 + [True])[required_cols]
        cleaner_data['rn'] = np.arange(len(cleaner_data)) + 1
        return self.adjust_cup_table_column_type(cleaner_data)

    def get_user_league_rank(self) -> dict:
        get_user_points = self.league_member_points()
        return {key: {sub[0]: sub[11] for sub in val} for key, val in get_user_points.items()}

    def get_game_points_players(self) -> dict:
        PlayerPrediction = self.get_top_players_predictions()
        PlayerReal = TopPlayerStats(self.user_id).get_relevant_players_for_league_points()
        output = {}
        league_map = {
            item['league_name']: item['id']
            for item in League.objects.all().values('id', 'league_name')
        }
        cols = ['user_id', 'event_type', 'player_name', 'player_name_long', 'nick_name', 'league_name']
        excluded_league_list = [24, 19, 31]
        for key, val in PlayerPrediction.items():
            user_list = {item['nick_name']: 0 for item in
                         LeagueMember.objects.filter(league_name_id=key).values('nick_name')}
            if league_map[key] not in excluded_league_list:
                df_prediction = pd.DataFrame(PlayerPrediction[key], columns=cols)
                df_prediction['event_type'] = np.where(df_prediction['event_type'] == 'top_scorer', 'Top Scorer',
                                                       np.where(df_prediction['event_type'] == 'top_assist',
                                                                'Top Assist', None))
                new_cols = ['user_id', 'nick_name', 'event_type', 'player_name', 'count']
                df_merged = pd.merge(df_prediction, PlayerReal, on=['player_name', 'event_type'], how='inner')[new_cols]
                df_output = df_merged.groupby(
                    ['user_id', 'nick_name', 'event_type', 'player_name']).first().reset_index()
                elm_count = list(df_output['nick_name'].values)
                output[key] = {item: elm_count.count(item) * 3 if item in list(set(elm_count)) else 0
                               for item in user_list}
            else:
                output[key] = user_list
        return output


class GameStats(UserPredictionBase):
    def __init__(self, user_id, match_label):
        super().__init__(user_id)
        self.match_label = match_label

    def match_prediction_df(self):
        df_input = self.present_predictions()
        output = {}
        if df_input[0] is not None:
            for key, obj in df_input[0].items():
                df = pd.DataFrame(obj)
                df.columns = df_input[1]
                df = df[df.match_label == self.match_label]
                df[['home_team', 'away_team']] = df.match_label.str.split('-', expand=True, n=1)[[0, 1]]
                df['pred_dir'] = np.where(df.pred_score_home > df.pred_score_away,
                                          df.home_team,
                                          np.where(df.pred_score_home < df.pred_score_away, df.away_team, 'Draw'))
                df['predicted_score_alternative'] = np.where(df['pred_dir'] == df.away_team,
                                                             df['pred_score_away'] + '-' + df['pred_score_home'],
                                                             df['predicted_score'])
                df_scores = pd.DataFrame(
                    df.groupby(['predicted_score_alternative', 'pred_dir'])['game_status'].count()).reset_index(). \
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

    def match_winner_df(self):
        df_input = self.present_predictions()
        output = {}
        if df_input[0] is not None:
            for key, obj in df_input[0].items():
                df = pd.DataFrame(obj)
                df.columns = df_input[1]
                df = df[df.match_label == self.match_label]
                df[['home_team', 'away_team']] = df.match_label.str.split('-', expand=True, n=1)[[0, 1]]
                df['pred_dir'] = np.where(df.pred_score_home > df.pred_score_away,
                                          df.home_team,
                                          np.where(df.pred_score_home < df.pred_score_away, df.away_team, 'Draw'))
                df_winner = pd.DataFrame(df.groupby(['pred_winner'])['game_status'].count()). \
                    reset_index().rename(columns={
                    'game_status': 'count',
                    'pred_winner': 'winner'
                })
                df_winner_output = df_winner
                output[key] = df_winner_output
            return output
        else:
            return None

    def match_live_game(self):
        df_input = self.present_predictions()
        output = {}
        if df_input[0] is not None:
            for key, obj in df_input[0].items():
                df = pd.DataFrame(obj)
                df.columns = df_input[1]
                df = df[df.match_label == self.match_label]
                df[['home_team', 'away_team']] = df.match_label.str.split('-', expand=True, n=1)[[0, 1]]
                output[key] = df
            return output
        else:
            return None

    @staticmethod
    def match_prediction_plot(data):
        fig = px.bar(
            data,
            x='score', y='count', color="winner", template='simple_white', text='count',
            title="Score Distribution", labels={"score": "Score", "count": "Prediction Count", "winner": ""})
        fig.update_traces(textposition='inside')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def match_winner_plot(data):
        fig = px.pie(data, values='count', names='winner', title='Predicted Winner')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def merge_dicts(a: dict, b: dict):
        new_output = {}
        for i, j in zip(a.items(), b.items()):
            if i[0] == j[0]:
                new_output[i[0]] = [i[1], j[1]]
        return new_output

    def match_prediction_outputs(self):
        dict_score = self.match_prediction_df()
        dict_winner = self.match_winner_df()
        if dict_score is not None:
            output_score = {key: self.match_prediction_plot(data) for key, data in dict_score.items()}
            output_winner = {key: self.match_winner_plot(data) for key, data in dict_winner.items()}
            return self.merge_dicts(output_score, output_winner)
        else:
            return None


class MailTemplate:
    def group_stage_bet_submission(self, request, form) -> dict:
        home, away, results, top_players = [], [], [], {}
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

    def knockout_bet_submission(self, request, form, stage: str) -> dict:
        home, away, results, winner = [], [], [], []
        for i in enumerate([(key, obj) for key, obj in form.cleaned_data.items() if key != 'user_name']):
            if i[0] % 3 == 0:
                home.append(i[1])
            elif i[0] % 3 == 1:
                away.append(i[1])
            elif i[0] % 3 == 2:
                winner.append(i[1])
        for h, a, w in zip(home, away, winner):
            result = f"{TGM[stage][h[0]]}-{TGM[stage][a[0]]}: {h[1]}-{a[1]}. Winner: {w[1]}"
            results.append(result)
        text_results = '\n'.join(results)
        subject = f"Euro 2021 Friends League - Email Confirmation - {stage} Bet Submission"
        message = f"Dear {request.user.username}!\n" \
                  f"You have just submitted successfully your bet form!\n" \
                  f"Please Note - you can easily edit your bets by 6 hours before first stage's match using the app 'edit your bet' tab.\n\n" \
                  f"For your convenience and our documentation, please find bellow your bets. \n\n" \
                  f"{text_results}\n\n" \
                  "Regards,\nLeague management team"
        return {'subject': subject, 'message': message}

    def user_joined_a_league(self, request, form) -> dict:
        subject = "Euro 2021 Friends League - Email Confirmation - League Membership"
        message = f"Dear {form.cleaned_data['first_name']}!\n" \
                  f"You are officially part of the {form.cleaned_data['league_name']} league. " \
                  f"Please make sure to submit your bets. Good luck!\n\n" \
                  "Regards,\nLeague management team"
        return {'subject': subject, 'message': message}


class BaseViewUserControl:
    def __init__(self, user_id):
        self.user_id = user_id

    def onboarding(self) -> dict:
        league_data = LeagueMember.objects.filter(user_name_id=self.user_id)
        image = UserImage.objects.filter(user_name_id=self.user_id)
        bet_data_group_stage = Game.objects.filter(user_name_id=self.user_id)
        bet_16 = GameTop16.objects.filter(user_name_id=self.user_id)
        bet_8 = GameTop8.objects.filter(user_name_id=self.user_id)
        bet_4 = GameTop4.objects.filter(user_name_id=self.user_id)
        bet_2 = GameTop2.objects.filter(user_name_id=self.user_id)
        context = {
            'league': True if len(league_data) > 0 else False,
            'bet': True if len(bet_data_group_stage) > 0 else False,
            'image': True if len(image) > 0 else False,
            'bet_top_16': True if len(bet_16) > 0 else False,
            'bet_top_8': True if len(bet_8) > 0 else False,
            'bet_top_4': True if len(bet_4) > 0 else False,
            'bet_top_2': True if len(bet_2) > 0 else False,
        }
        return context


class GetMatchData:
    def __init__(self):
        self.TOKEN = 'bfa132288504de6860c8ae3259d21fa7'
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'
        self.L_API_PREFIX = f"http://livescore-api.com/api-client/"
        self.L_API_SUFFIX = f".json&competition_id=387&?key=KDbVwkzQSt1r7tCq&secret=ZS5RT5WXc7HyvUMgyXb4iLVaeWClqfMq"

    def extract_data(self):
        data = requests.get(url=self.URL).json()
        return data

    def all_matches_phase_1(self):
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
                       home_team_score, away_team, away_team_id, away_team_score, match_label
                       ]
                output.append(row)
        fields = ['match_day_id', 'match_round', 'match_day_playoff', 'match_day_type', 'match_day_start',
                  'match_day_end', 'match_id', 'match_status', 'match_date', 'match_hour', 'home_team',
                  'home_team_id', 'home_team_score', 'away_team', 'away_team_id', 'away_team_score', 'match_label',
                  ]
        return output, fields

    def get_knockout_attributes(self, match_id):
        base_url = f"{self.PREFIX}/matches/{match_id}&apikey={self.TOKEN}"
        data = requests.get(url=base_url).json()
        score_90_min_home = int(data['match']['homeParticipant']['score']) - int(
            data['match']['extraTime']['home_score'])
        score_90_min_away = int(data['match']['awayParticipant']['score']) - int(
            data['match']['extraTime']['away_score'])
        extra_time = True if data['match']['extraTime']['is_extra'] == '1' else False
        penalties = False
        if 'stages' in data.keys():
            if data['stages']:
                stage_types = [i[1] for i in [list(item.values()) for item in data['stages']]]
                if 'Penalty Shootout' in stage_types:
                    loc = stage_types.index('Penalty Shootout')
                    if data['stages'][loc]['home_score'] is not None:
                        penalties = True
        if penalties:
            stage_score = data['stages'][loc]
            game_winner = 'home' if int(stage_score['home_score']) > int(stage_score['away_score']) \
                else 'away' if int(stage_score['home_score']) < int(stage_score['away_score']) else 'draw'
        else:
            game_winner = 'home' if int(data['match']['homeParticipant']['score']) > \
                                    int(data['match']['awayParticipant']['score']) else \
                'away' if int(data['match']['homeParticipant']['score']) < int(
                    data['match']['awayParticipant']['score']) \
                    else 'draw'
        context = {
            'is_extra_time': extra_time,
            'home_score_90_min': score_90_min_home,
            'away_score_90_min': score_90_min_away,
            'home_score_end_match': data['match']['homeParticipant']['score'],
            'away_score_end_match': data['match']['awayParticipant']['score'],
            'match_winner': game_winner
        }
        return context

    def all_matches(self):
        data, fields = self.all_matches_phase_1()
        for row in data:
            if row[2] == '1':
                extra_time_info = [*self.get_knockout_attributes(row[6]).values()]
                row += extra_time_info
            else:
                row += [None] * 5
        fields += ['is_extra_time', 'home_score_90_min', 'away_score_90_min',
                   'home_score_end_match', 'away_score_end_match', 'match_winner']
        for row in data:
            row[12] = int(row[18]) if 'Final' in row[1] else row[12]
            row[15] = int(row[19]) if 'Final' in row[1] else row[15]
        return data, fields

    def all_matches_old(self):
        data = self.extract_data()
        # live_api_history = self.match_history_data()
        # live_api_realtime = self.match_live_data()
        live_api_history_matches = None  # [item for item in live_api_history.keys()]
        live_api_realtime_matches = None  # [item for item in live_api_realtime.keys()] if live_api_realtime is not None else [ None]
        live_fields = ['full_time_score', 'match_winner', '90min_home_team_score', '90min_away_team_score']
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
                       home_team_score, away_team, away_team_id, away_team_score, match_label
                       ]
                # if match_label in live_api_realtime_matches:
                #     extra_data = [live_api_realtime[match_label][item] for item in live_fields]
                # elif match_label in live_api_history_matches:
                #     extra_data = [live_api_history[match_label][item] for item in live_fields]
                #     row += extra_data + [True]
                # else:
                #     row += [None for item in live_fields] + [False]
                output.append(row)
        fields = ['match_day_id', 'match_round', 'match_day_playoff', 'match_day_type', 'match_day_start',
                  'match_day_end', 'match_id', 'match_status', 'match_date', 'match_hour', 'home_team',
                  'home_team_id', 'home_team_score', 'away_team', 'away_team_id', 'away_team_score', 'match_label',
                  # 'live_ft_score', 'live_match_winner', 'live_90_home_score', 'live_90_away_score', 'is_enriched'
                  ]
        return output, fields

    def match_history_data(self):
        url_history = f"{self.L_API_PREFIX}scores/history{self.L_API_SUFFIX}"
        data_history = requests.get(url=url_history).json()
        total_pages = data_history['data']['total_pages']
        output = {}
        for j in range(1, total_pages + 1):
            page_matches = data_history['data']['match']
            for item in page_matches:
                match_label = f"{item['home_name']}-{item['away_name']}".replace('FYR', 'North')
                outcomes = item['outcomes']
                winner = outcomes['full_time'] if outcomes['extra_time'] is None else outcomes['extra_time']
                output[match_label] = {
                    'full_time_score': item['ft_score'].replace(' - ', '-'),
                    'match_winner': 'home' if winner == '1' else 'away' if winner == '2' else 'draw',
                    '90min_home_team_score': item['ft_score'].split(' - ')[0],
                    '90min_away_team_score': item['ft_score'].split(' - ')[1],
                    '90min_score_label': item['ft_score']
                }
            if j < total_pages:
                next_page = data_history['data']['next_page']
                data_history = requests.get(url=next_page).json()
        return output

    def match_live_data(self):
        url_live = f"{self.L_API_PREFIX}scores/live{self.L_API_SUFFIX}"
        data_live = requests.get(url=url_live).json()
        if len(data_live['data']['match']) == 0:
            return None
        else:
            output = {}
            page_matches = data_live['data']['match']
            for item in page_matches:
                match_label = f"{item['home_name']}-{item['away_name']}".replace('FYR', 'North')
                outcomes = item['outcomes']
                winner = outcomes['full_time'] if outcomes['extra_time'] is None else outcomes['extra_time']
                output[match_label] = {
                    'full_time_score': item['ft_score'].replace(' - ', '-'),
                    'match_winner': 'home' if winner == '1' else 'away' if winner == '2' else 'draw',
                    '90min_home_team_score': item['ft_score'].split(' - ')[0],
                    '90min_away_team_score': item['ft_score'].split(' - ')[1],
                    '90min_score_label': item['ft_score']
                }
            return output

    def game_router(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        next_df = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
        next_output = next_df.head(1).reset_index()
        next_game_status = 'live' if next_output['match_status'][0] == '-1' else 'fixture'
        if next_game_status == 'live':
            prev_df = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
            prev_output = prev_df.head(2).tail(1).reset_index()
        else:
            prev_df = df[df.match_status == '1'].sort_values(by=['match_date', 'match_hour'])
            prev_output = prev_df.tail(1).reset_index()
        context = {
            'next': {
                'data': {key: obj[0] for key, obj in next_output.head(1).to_dict().items()},
                'logo': {
                    next_output.home_team[0]: teams[next_output.home_team[0]]['logo'],
                    next_output.away_team[0]: teams[next_output.away_team[0]]['logo']
                }
            },
            'prev': {
                'data': {key: obj[0] for key, obj in prev_output.head(1).to_dict().items()},
                'logo': {
                    prev_output.home_team[0]: teams[prev_output.home_team[0]]['logo'],
                    prev_output.away_team[0]: teams[prev_output.away_team[0]]['logo']
                }
            },
            'started_games': int(df[df.match_status != '0'].shape[0])
        }
        return context

    def game_router2(self, df2):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        next_df = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
        next_output = next_df.head(1).reset_index()
        next_game_status = 'live' if next_output['match_status'][0] == '-1' else 'fixture'
        if next_game_status == 'live':
            prev_df = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
            prev_output = prev_df.head(2).tail(1).reset_index()
        else:
            prev_df = df[df.match_status == '1'].sort_values(by=['match_date', 'match_hour'])
            prev_output = prev_df.tail(1).reset_index()
        context = {
            'next': {
                'data': {key: obj[0] for key, obj in next_output.head(1).to_dict().items()},
                'logo': {
                    next_output.home_team[0]: teams[next_output.home_team[0]]['logo'],
                    next_output.away_team[0]: teams[next_output.away_team[0]]['logo']
                }
            },
            'prev': {
                'data': {key: obj[0] for key, obj in prev_output.head(1).to_dict().items()},
                'logo': {
                    prev_output.home_team[0]: teams[prev_output.home_team[0]]['logo'],
                    prev_output.away_team[0]: teams[prev_output.away_team[0]]['logo']
                }
            },
            'started_games': int(df[df.match_status != '0'].shape[0])
        }
        return context

    def top_players(self, event_type: int = 1) -> list:
        event_name = 'Top Scorer' if event_type == 1 else 'Top Assist'
        url = f'{self.PREFIX}/topplayers/40&apikey={self.TOKEN}&event_id={str(event_type)}&limit=1000'
        top_player_api = requests.get(url=url).json()['season']['players']
        top_player_list = [[item['shortname'], item['teamname'], int(item['eventCount']), f'{event_name}']
                           for item in top_player_api]
        top_player_list_adjusted = []
        for item in top_player_list:
            if [*item] == ['C. Ronaldo', 'Portugal', 2, 'Top Scorer']:
                top_player_list_adjusted.append(['C. Ronaldo', 'Portugal', 5, 'Top Scorer'])
            else:
                top_player_list_adjusted.append(item)
        df = pd.DataFrame(top_player_list_adjusted).sort_values(by=2, ascending=False)
        return df.values.tolist()


class TopPlayerStats(GetMatchData):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @staticmethod
    def get_minimal_count_value(df) -> int:
        sorted_df = pd.DataFrame(df['count'].value_counts()).reset_index().sort_values(by='index', ascending=False)
        event_details = {item[0]: item[1] for item in sorted_df.values.tolist()}
        agg = 0
        for key, val in event_details.items():
            agg += val
            if agg >= 3:
                return int(key)

    def top_players_real(self) -> tuple:
        scorers = self.top_players(1)
        assists = self.top_players(2)
        players_dict = {'top_scorer': scorers, 'top_assists': assists}
        cols = ['player_name', 'team', 'count', 'event_type']
        df = pd.DataFrame(scorers + assists, columns=cols)
        return players_dict, df

    def get_relevant_players_for_league_points(self) -> dict:
        df = self.top_players_real()[1]
        df_goal = df[df.event_type == 'Top Scorer']
        df_assists = df[df.event_type == 'Top Assist']
        adj_df_scorers = df_goal[df_goal['count'] >= self.get_minimal_count_value(df_goal)]
        adj_df_df_assists = df_assists[df_assists['count'] >= self.get_minimal_count_value(df_assists)]
        return pd.concat([adj_df_scorers, adj_df_df_assists])

    @staticmethod
    def build_plot(data: dict):
        fig = px.bar(data, x='score', y='count', color="winner", template='simple_white', text='count',
                     title="Score Distribution", labels={"score": "Score", "count": "Prediction Count", "winner": ""})
        fig.update_traces(textposition='inside')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def unique(list1):
        unique_list = []
        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list

    @staticmethod
    def ranked_items(x):
        seq = sorted(x)
        index = [seq.index(v) for v in x]
        return index

    def data_sankey_top_players(self, data, event_type) -> dict:
        relevant_data = [item for item in data if item[1] == event_type]
        predicted_player = [obj[2] for obj in relevant_data]
        user_ids = [obj[0] for obj in relevant_data]
        unique_user_ids = self.unique(user_ids)
        ranked_unique_user_ids = self.ranked_items(unique_user_ids)
        source_map = {key: val for key, val in zip(unique_user_ids, ranked_unique_user_ids)}
        source = [source_map[i] for i in user_ids]
        users = [obj[4] for obj in relevant_data]
        unique_users = self.unique(users)
        unique_players = self.unique(predicted_player)
        label = unique_users + unique_players
        n_start, n_players = len(ranked_unique_user_ids), len(unique_players)
        n_end = n_players + n_start + 1
        player_id = {obj: key for key, obj in zip(range(n_start, n_end), unique_players)}
        target = [player_id[obj[2]] for obj in relevant_data]
        value = [1 for _ in source]
        return {'source': source, 'target': target, 'value': value, 'label': label}

    def data_sankey_live_game(self, data, league_name: str) -> dict:
        predicted_result = [obj[1] for obj in data]
        user_ids = [obj[3] for obj in data]
        unique_user_ids = self.unique(user_ids)
        ranked_unique_user_ids = self.ranked_items(unique_user_ids)
        source_map = {key: val for key, val in zip(unique_user_ids, ranked_unique_user_ids)}
        source = [source_map[i] for i in user_ids]
        users = [obj[0] for obj in data]
        unique_users_pre = self.unique(users)
        user_rank_map = UserPredictionBase(self.user_id).get_user_league_rank()[league_name]
        unique_users = [f"{item} ({user_rank_map[item]})" for item in unique_users_pre]
        unique_results = self.unique(predicted_result)
        label = unique_users + unique_results
        n_start, n_results = len(ranked_unique_user_ids), len(unique_results)
        n_end = n_results + n_start + 1
        result_id = {obj: key for key, obj in zip(range(n_start, n_end), unique_results)}
        target = [result_id[obj[1]] for obj in data]
        value = [1 / (0.1 if item[2] == 0 else item[2]) for item in data]
        return {'source': source, 'target': target, 'value': value, 'label': label}

    @staticmethod
    def build_sankey_plot(data: dict) -> dict:
        link = dict(source=data['source'], target=data['target'], value=data['value'])
        node = dict(label=data['label'], pad=40, thickness=5)
        plot_data = go.Sankey(link=link, node=node)
        fig = go.Figure(plot_data)
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT, )
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    def top_players_pred_plot(self) -> dict:
        data = UserPredictionBase(user_id=self.user_id).get_top_players_predictions()
        output = {}
        for key, val in data.items():
            scorers_data = self.data_sankey_top_players(val, 'top_scorer')
            assists_data = self.data_sankey_top_players(val, 'top_assist')
            output[key] = {
                'top_scorer': self.build_sankey_plot(scorers_data),
                'top_assist': self.build_sankey_plot(assists_data)
            }
        return output

    @staticmethod
    def score_distance(score_list: list) -> int:
        if score_list[2] > score_list[0] or score_list[3] > score_list[1]:
            return 15
        else:
            home_distance = score_list[0] - score_list[2]
            away_distance = score_list[1] - score_list[3]
            return home_distance + away_distance

    @staticmethod
    def get_live_winning_users(data, ids: dict, images: dict, match_label: str):
        output = {}
        for key, val in data.items():
            base_data = []
            is_playoff = False
            for item in val:
                if item[3] == match_label:
                    if 'Final' not in item[12]:
                        base_data_row = [item[0]] + [*item[7:11]] + [None, None]
                    else:
                        is_playoff = True
                        home, away = match_label.split('-')
                        real_winner = home if item[15] == 'home' else away if item[15] == 'away' else item[16]
                        base_data_row = [item[0], item[7], item[8], item[17], item[18], item[14], real_winner]
                    base_data.append(base_data_row)
            df = pd.DataFrame(base_data, columns=['nick', 'p_h', 'p_a', 'r_h', 'r_a', 'pred_winner', 'real_winner'])
            if is_playoff:
                df['user_type'] = np.where(((df.p_h == df.r_h) & (df.p_a == df.r_a)),
                                           'boomer',
                                           np.where(df.pred_winner == df.real_winner, 'winner', 'Loser'))
            else:
                df['user_type'] = np.where(((df.p_h == df.r_h) & (df.p_a == df.r_a)), 'boomer',
                                           np.where(
                                               ((df.p_h > df.p_a) & (df.r_h > df.r_a)) |
                                               ((df.p_h == df.p_a) & (df.r_h == df.r_a)) |
                                               ((df.p_h < df.p_a) & (df.r_h < df.r_a))
                                               , 'winner', 'Loser'))
            adj_img_dict = {}
            relevant_users = [ids[i] for i in list(df[df.user_type != 'Loser']['nick'].unique())]
            for uid in relevant_users:
                adj_img_dict[uid] = f"{AWS_S3_URL}{images[uid]}" if uid in [i for i in
                                                                            images.keys()] else f"{AWS_S3_URL}{DEFAULT_PHOTO}"
            output[key] = {
                'Boomers': [[item, ids[item], adj_img_dict[ids[item]]] for item in
                            df[df.user_type == 'boomer']['nick']],
                'Winners': [[item, ids[item], adj_img_dict[ids[item]]] for item in df[df.user_type == 'winner']['nick']]
            }
        return output

    def live_game_plot(self, match_label: str) -> dict:
        BaseClassData = UserPredictionBase(user_id=self.user_id)
        relevant_user_ids = BaseClassData.extract_relevant_user_ids()
        data = BaseClassData.present_predictions()[0]
        league_members_data = list(
            LeagueMember.objects.filter(user_name_id__in=relevant_user_ids).values('user_name_id', 'nick_name'))
        user_id_map = {item['nick_name']: item['user_name_id'] for item in league_members_data}
        unique_user_ids = list(set([item for item in user_id_map.values()]))
        user_image = {item['user_name_id']: item['header_image']
                      for item in list(UserImage.objects.filter(user_name_id__in=unique_user_ids).values())}
        output = {}
        for key, val in data.items():
            init_data = [[
                item[0],
                item[4],
                self.score_distance([int(i) for i in item[7:11]]) if 'Final' not in item[12] else
                self.score_distance([int(i) for i in [item[7], item[8], item[19], item[20]]]),
                user_id_map[item[0]]
            ] for item in val if item[3] == match_label]
            relevant_data = [item for item in init_data if item[2] < 15]
            data_preps = self.data_sankey_live_game(relevant_data, league_name=key)
            output[key] = self.build_sankey_plot(data_preps)
        return output, self.get_live_winning_users(data, user_id_map, user_image, match_label)





class CupKnockOut(UserPredictionBase):
    def __init__(self, user_id, beta: bool = False):
        super().__init__(user_id)
        self.beta = beta
        self.draw_template = CUP_DRAW if not self.beta else CUP_DRAW_BETA
        self.league_id = 9 if not self.beta else 1

    def get_league_name(self):
        league_name = list(League.objects.filter(id=self.league_id).values('league_name'))[0]['league_name']
        return league_name

    def get_user_data(self):
        league_name = self.get_league_name()
        league_members = list(
            LeagueMember.objects.filter(league_name_id=league_name).values('user_name_id', 'nick_name'))
        user_list = [i['user_name_id'] for i in league_members]
        get_image = pd.DataFrame(list(UserImage.objects.filter(user_name_id__in=user_list).all().
                                      order_by('user_name_id', '-created').values('user_name_id', 'header_image'))). \
            groupby(['user_name_id']).first().reset_index().values.tolist()
        league_images = {item[0]: item[1] for item in get_image}
        league_members_map = {item['user_name_id']: item['nick_name'] for item in league_members}
        for key, val in league_members_map.items():
            img = league_images[key] if key in list(league_images.keys()) else DEFAULT_PHOTO
            league_members_map[key] = {
                'nick': league_members_map[key],
                'img': f"{AWS_S3_URL}{img}"
            }
        return league_members_map

    def prepare_template_data(self):
        league_name = self.get_league_name()
        metadata = self.present_predictions()
        col_names = metadata[1]
        df = pd.DataFrame(metadata[0][league_name], columns=col_names)
        user_data = self.get_user_data()
        output = {}
        for stage in ['1/8 Final', '1/4 Final']:
            output[stage] = {}
            for key, val in self.draw_template[stage]['data'].items():
                users = [user_data[item['user_id']]['nick'] for item in val.values()]
                user_ids = [item['user_id'] for item in val.values()]
                sub_df = df[(df.nick_name.isin(users)) & (df.match_type == stage)]
                if sub_df.shape[0] > 0:
                    mini_league = self.get_game_points_cup(sub_df)
                    output[stage][key] = {
                        'logos': {user: user_data[uid]['img'] for user, uid in zip(users, user_ids)},
                        'table': mini_league,
                        'winner': mini_league[0][0],
                        'matches': self.present_match_games_data(sub_df)
                    }
                else:
                    output[stage][key] = None
        return output

    @staticmethod
    def manipulate_prediction_presentation(data):
        player_a = [data[i] for i in range(len(data)) if i % 2 != 0]
        player_b = [data[i] for i in range(len(data)) if i % 2 == 0]
        merged = [[a[0], a[2], a[4], a[1], a[3], a[5], b[0], b[2], b[4], a[6]] for a, b in zip(player_a, player_b)]
        context = [{
            'p1': i[0],
            'p1_pred': f"{i[1]} ({i[2]})",
            'actual_match': f"{i[3]}",
            'actual_score': f"{i[4]} ({i[5]})" if i[9] != 'Fixture' else f"{i[4]}",
            'p2': i[6],
            'p2_pred': f"{i[7]} ({i[8]})",
            'status': i[9]
        } for i in merged]
        return context

    def present_match_games_data(self, df):
        df[['home_team', 'away_team']] = df.match_label.str.split('-', n=2, expand=True)
        df['home_score_90_min'] = df['home_score_90_min'].astype(int)
        df['away_score_90_min'] = df['away_score_90_min'].astype(int)
        df['real_score_90_min'] = df['home_score_90_min'].map(str) + '-' + df['away_score_90_min'].map(str)
        df['knockout_winner_team'] = np.where(df.knockout_winner == 'home',
                                              df.home_team,
                                              np.where(df.knockout_winner == 'away', df.away_team, 'draw'))
        cols = ['nick_name', 'match_label', 'predicted_score', 'real_score_90_min',
                'pred_winner', 'knockout_winner_team', 'game_status']
        output = df[cols].values.tolist()
        return self.manipulate_prediction_presentation(output)

