from data.teams import team_game_map
from myapp.models import *
import plotly.graph_objects as go
import numpy as np
from myproject.settings import MEDIA_URL, AWS_S3_URL, DEFAULT_PHOTO
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
import plotly.graph_objects as go
from data.knockout import TEAM_GAME_MAP as TGM, CUP_GAMES

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


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


class UserPredictionBase:
    def __init__(self, user_id):
        self.TOKEN = env('API_TOKEN')
        self.PREFIX = 'https://api.statorium.com/api/v1'
        self.URL = f'{self.PREFIX}/matches/?season_id=40&apikey={self.TOKEN}'
        self.user_id = user_id

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

    def user_game_bet_id(self) -> dict:
        data = Game.objects.filter(user_name_id=self.user_id)
        if len(data) > 0:
            return data[0].id
        else:
            return None

    def extract_relevant_user_ids(self) -> list:
        leagues = list(LeagueMember.objects.filter(user_name_id=self.user_id).values('league_name'))
        ids = list(LeagueMember.objects.filter(league_name_id__in=[i['league_name'] for i in leagues]).values('user_name_id'))
        return [i['user_name_id'] for i in ids]

    @staticmethod
    def extract_group_stage_predictions(ids: list):
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id__in=ids).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('top_')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home', np.where(df.variable.str[-1:] == '1', 'Away', None))
        df['game_id'] = df.variable.str[4:-2]
        df['predicted_score'] = df['value'].astype(str)
        df_main = df.sort_values(by=['user_name_id', 'variable', 'location']).groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[[0, 1]]
        df_main['pred_winner'] = None
        return df_main

    @staticmethod
    def extract_knockout_predictions(df_init):
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('_alt')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home', np.where(df.variable.str[-1:] == '1', 'Away', None))
        df['game_id'] = df.variable.str[4:6]
        df['predicted_score'] = df['value'].astype(str)
        df_score = df[df.location.notnull()]
        df_winner = df[~df.location.notnull()][['user_name_id', 'game_id', 'value']]
        df_main = df_score.sort_values(by=['user_name_id', 'variable', 'location']).\
            groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[[0, 1]]
        output = pd.merge(df_main, df_winner, on=['user_name_id', 'game_id'], how='inner').rename(columns={'value': 'pred_winner'})
        return output

    def get_user_prediction(self):
        relevant_ids = self.extract_relevant_user_ids()
        df_main = self.extract_group_stage_predictions(relevant_ids)
        df_init_top_16 = pd.DataFrame(list(GameTop16.objects.filter(user_name_id__in=relevant_ids).values()))
        if df_init_top_16.shape[0] > 0:
            df_top_16 = self.extract_knockout_predictions(df_init_top_16)
            df_main = df_main.append(df_top_16)
            df_init_top_8 = pd.DataFrame(list(GameTop8.objects.filter(user_name_id__in=relevant_ids).values()))
            if df_init_top_8.shape[0] > 0:
                df_top_8 = self.extract_knockout_predictions(df_init_top_8)
                df_main = df_main.append(df_top_8)
                df_init_top_4 = pd.DataFrame(list(GameTop4.objects.filter(user_name_id__in=relevant_ids).values()))
                if df_init_top_4.shape[0] > 0:
                    df_top_4 = self.extract_knockout_predictions(df_init_top_4)
                    df_main = df_main.append(df_top_4)
                    df_init_top_2 = pd.DataFrame(list(GameTop2.objects.filter(user_name_id__in=relevant_ids).values()))
                    if df_init_top_2.shape[0] > 0:
                       df_top_2 = self.extract_knockout_predictions(df_init_top_4)
                       df_main = df_main.append(df_top_2)
        return df_main

    def get_user_prediction_b(self):
        relevant_ids = self.extract_relevant_user_ids()
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id__in=relevant_ids).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[~df.variable.str.contains('top_')]
        df['location'] = np.where(df.variable.str[-1:] == '0', 'Home', 'Away')
        df['game_id'] = df.variable.str[4:-2]
        df['predicted_score'] = df['value'].astype(str)
        df_main = df.sort_values(by=['user_name_id', 'variable', 'location']).groupby(['user_name_id', 'game_id'])['predicted_score'].apply('-'.join).reset_index()
        df_main[['pred_score_home', 'pred_score_away']] = df_main.predicted_score.str.split('-', expand=True, n=1)[[0, 1]]
        return df_main

    def fetch_user_league_membership_data(self, user_id):
        relevant_ids = self.extract_relevant_user_ids()
        league_member_fields = ['user_name_id', 'first_name', 'last_name', 'league_name_id', 'nick_name', 'created']
        df_league_member_pre = pd.DataFrame(list(LeagueMember.objects.filter(user_name_id__in=relevant_ids).values()))[league_member_fields].\
            sort_values(by=['user_name_id', 'league_name_id', 'created'], ascending=[True, True, False])
        leagues = list(df_league_member_pre[df_league_member_pre.user_name_id == user_id].league_name_id.unique())
        df_league_member = df_league_member_pre.groupby(['user_name_id', 'league_name_id']).first().\
            reset_index().drop(columns='created')
        return df_league_member[df_league_member.league_name_id.isin(leagues)]

    def get_top_players_predictions(self) -> dict:
        relevant_ids = self.extract_relevant_user_ids()
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id__in=relevant_ids).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[df.variable.str.contains('top_')]
        df['player_name'] = df.value.str.split(' - ', expand=True, n=1)[[1]]
        df['variable_type'] = df.variable.str[:-2]
        df_predictions = df[['user_name_id', 'variable_type', 'player_name', 'value']]
        df_league = self.fetch_user_league_membership_data(self.user_id)[['user_name_id', 'nick_name', 'league_name_id']]
        output_df = pd.merge(df_predictions, df_league, on='user_name_id', how='inner')
        leagues = list(output_df.league_name_id.unique())
        output = {league: output_df[output_df.league_name_id == league].values.tolist() for league in leagues}
        return output

    def get_top_players_my_predictions(self) -> dict:
        df_init = pd.DataFrame(list(Game.objects.filter(user_name_id=self.user_id).values()))
        df = df_init.drop(columns=['created', 'updated', 'id']).sort_values(by='user_name_id').\
            groupby('user_name_id').first().reset_index().melt(id_vars='user_name_id')
        df = df[df.variable.str.contains('top_')]
        df['player_name'] = df.value.str.split(' - ', expand=True, n=1)[[1]]
        df['event_type'] = df.variable.str[:-2]
        df_predictions = df[['user_name_id', 'event_type', 'player_name', 'value']]
        df_predictions['event_type'] = np.where(df_predictions['event_type'] == 'top_scorer', 'Top Scorer', 'Top Assist')
        df_real_players = TopPlayerStats(self.user_id).top_players_real()
        df_output = pd.merge(df_predictions, df_real_players[1], on=['player_name', 'event_type'], how='left')
        output = {item: df_output[df_output.event_type == item][['player_name', 'team', 'count']].values.tolist()
                  for item in ['Top Scorer', 'Top Assist']}
        return output

    def data_enrichment(self):
        extra_fields = ['game_id', 'match_label', 'real_score', 'real_score_home', 'real_score_away',
                        'game_status', 'date', 'hour', 'is_playoff', 'match_type', 'home_team', 'away_team', 'knockout_winner']
        metadata = self.get_api_data()
        df_main = self.get_user_prediction()
        df_api_enrichment = [
                 [
                    key,
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
                    None if val['is_playoff'] != '1' else val['home_team'] if val['real_score_home'] > val['real_score_away'] else val['away_team']
            ] for key, val in metadata.items()]
        df_more_data = pd.DataFrame(df_api_enrichment, columns=extra_fields)
        df_main_2 = pd.merge(
                    df_main,
                    df_more_data,
                    on=['game_id'],
                    how='inner')
        league_member_fields = ['user_name_id', 'first_name', 'last_name', 'league_name_id', 'nick_name', 'created']
        df_league_member_pre = pd.DataFrame(
            list(LeagueMember.objects.filter(user_name_id__in=self.extract_relevant_user_ids()).
                 values()))[league_member_fields].sort_values(
                                by=['user_name_id', 'league_name_id', 'created'],
                                ascending=[True, True, False])
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
            'real_score_away',
            'is_playoff',
            'match_type',
            'home_team',
            'away_team',
            'pred_winner',
            'knockout_winner'
            ]
        return output[output_fields]

    def present_predictions(self) -> tuple:
        data = self.data_enrichment()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        if len(leagues) > 0:
            output = {}
            required_fields = ['nick_name', 'date', 'hour', 'match_label', 'predicted_score', 'real_score',
                               'game_status', 'pred_score_home', 'pred_score_away', 'real_score_home',
                               'real_score_away', 'user_name_id', 'match_type', 'is_playoff', 'pred_winner', 'knockout_winner']
            for item in leagues:
                filtered_df = data[(data.league_name_id == item)][required_fields]
                filtered_df['status_rank'] = np.where(filtered_df.game_status == 'Finished', 1, 0)
                final_df = filtered_df.sort_values(by=['status_rank', 'date', 'hour']).drop(columns='status_rank')
                output[item] = final_df.values.tolist()
            return output, required_fields
        else:
            return None, None

    def present_my_predictions(self):
        data = self.data_enrichment()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        if len(leagues) > 0:
            output = {}
            required_fields = ['nick_name', 'date', 'hour', 'match_label', 'predicted_score', 'real_score',
                               'game_status', 'pred_score_home', 'pred_score_away', 'real_score_home',
                               'real_score_away', 'user_name_id', 'pred_winner']
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
        x['is_boom'] = np.where((x.pred_score_home == x.real_score_home) & (x.pred_score_away == x.real_score_away), 1, 0)
        return x

    def user_game_points(self):
        data = self.data_enrichment()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        next_game = GetMatchData().next_match().match_label[0]
        prev_game = GetMatchData().prev_match().match_label[0]
        if len(leagues) > 0:
            output = {}
            for item in leagues:
                x = {
                    'next': self.add_game_attributes(data, item, next_game),
                    'prev': self.add_game_attributes(data, item, prev_game)
                }
                boomers = {key: list(val[val.is_boom == 1].nick_name) for key, val in x.items()}
                winners = {key: list(np.setdiff1d(list(val[val.is_direction == 1].nick_name), boomers[key])) for key, val in x.items()}

                user_pred_df_next = x['next'].loc[x['next'].user_name_id == self.user_id]
                user_pred_df_prev = x['prev'].loc[x['prev'].user_name_id == self.user_id]
                user_nick = user_pred_df_next.nick_name.values[0]
                user_pred = {
                    'next': user_pred_df_next.predicted_score.values[0],
                    'prev': user_pred_df_prev.predicted_score.values[0]
                    }
                user_score = {key: 'Boom' if user_nick in value else '' for key, value in boomers.items()}
                output[item] = {'boom': boomers, 'winner': winners, 'user_pred': user_pred, 'user_score': user_score}
            reshaped_output = {key: {
                            'next': {
                                'boom': value['boom']['next'],
                                'winner': value['winner']['next'],
                                'user_pred': value['user_pred']['next'],
                                'user_score': value['user_score']['next']
                            },
                            'prev': {
                                'boom': value['boom']['prev'],
                                'winner': value['winner']['prev'],
                                'user_pred': value['user_pred']['prev'],
                                'user_score': value['user_score']['prev']
                           }
                        } for key, value in output.items()}
            return reshaped_output
        else:
            return None

    def home_screen_match_relevant_data(self):
        Match = GetMatchData()
        next_match_df = Match.next_match()
        prev_match_df = Match.prev_match()
        next_match = {key: obj[0] for key, obj in next_match_df.head(1).to_dict().items()}
        prev_match = {key: obj[0] for key, obj in prev_match_df.head(1).to_dict().items()}
        user_data = self.user_game_points()
        if isinstance(user_data, dict):
            some_league = list(user_data.keys())[0]
            next_match['user_pred'] = user_data[some_league]['next']['user_pred']
            prev_match['user_pred'] = user_data[some_league]['prev']['user_pred']
            return prev_match, next_match, user_data
        else:
            return None, None, None

    @staticmethod
    def table_calculations(x):
        x['pred_dir'] = np.where(x.pred_score_home > x.pred_score_away, 'home', np.where(x.pred_score_home < x.pred_score_away, 'away', 'draw'))
        x['real_dir'] = np.where(x.real_score_home > x.real_score_away, 'home', np.where(x.real_score_home < x.real_score_away, 'away', 'draw'))
        x['is_direction'] = np.where(x.pred_dir == x.real_dir, 1, 0)
        x['is_boom'] = np.where((x.pred_score_home == x.real_score_home) & (x.pred_score_away == x.real_score_away), 1, 0)
        x['is_knockout_boom'] = np.where((x.is_playoff == '1') & (x.pred_score_home == x.real_score_home) & (x.pred_score_away == x.real_score_away), 1, 0)
        x['is_knockout_direction'] = np.where((x.is_playoff == '1') & (x.pred_winner == x.knockout_winner), 1, 0)
        x['knockout_points'] = np.where((x.is_knockout_direction == 1) & (x.is_knockout_boom == x.knockout_winner), 4,
                                        np.where((x.is_knockout_direction != 1) & (x.is_knockout_boom == 1),
                                                 3,
                                        np.where((x.is_knockout_direction == 1) & (x.is_knockout_boom != 1), 1, 0)))
        x['points'] = np.where(x.is_playoff != '1',
                               np.where(x.is_boom == 1, 3, np.where(x.is_direction == 1, 1, 0)),
                               x['knockout_points'])
        x['started'] = np.where(x.game_status != 'Fixture', 1, 0)
        x['is_live'] = np.where(x.game_status == 'live', 1, 0)
        x['distance'] = (abs(x.real_score_home.astype(int) - x.pred_score_home.astype(int))) + \
                        (abs(x.real_score_away.astype(int) - x.pred_score_away.astype(int)))
        d = [
            int(x['started'].sum()),
            int((x['started'] * x['points']).sum()),
            int((x['started'] * x['is_boom']).sum()),
            int((x['started'] * x['is_direction']).sum()),
            round((x['started'] * x['points']).sum()*100/(x['started'] * 3).sum(), 1),
            int((x['started'] * x['is_boom'] * (x['pred_score_home'].astype(int) + x['pred_score_away'].astype(int))).sum()),
            int((x['is_live'] * x['points']).sum()),
            int(1),
            int((x['started'] * x['distance']).sum())
        ]
        index_names = ['games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'live_points', 'players', 'distance']
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
            return None

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
        required_cols = ['nick_name', 'games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'live_points', 'distance', 'user_name_id']
        data = pd.DataFrame(df.groupby(['user_name_id', 'nick_name']).apply(self.table_calculations).reset_index())
        df = pd.DataFrame(self.adjust_table_column_type(data[required_cols]), columns=required_cols)
        df['player_point_col'] = [int(player_points[item[1]]) for item in data.values.tolist()]
        df['points'] = df['player_point_col'] + df['points']
        cleaner_data = df.sort_values(by=['points', 'boom', 'direction', 'predicted_goals', 'distance'],
                                      ascending=[False]*4 + [True])
        cleaner_data['rn'] = np.arange(len(cleaner_data)) + 1
        return cleaner_data.values.tolist()

    def get_game_points_cup(self, df):
        required_cols = ['nick_name', 'games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'live_points', 'distance',  'user_name_id']
        data = pd.DataFrame(df.groupby(['user_name_id', 'nick_name']).apply(self.table_calculations).reset_index())
        cleaner_data = data.sort_values(
                            by=[('points',), ('boom',), ('direction', ), ('predicted_goals', ), ('distance', )],
                            ascending=[False]*4 + [True])[required_cols]
        cleaner_data['rn'] = np.arange(len(cleaner_data)) + 1
        return self.adjust_table_column_type(cleaner_data)

    def get_user_league_rank(self) -> dict:
        get_user_points = self.league_member_points()
        return {key: {sub[0]: sub[11] for sub in val} for key, val in get_user_points.items()}

    def get_game_points_knockout(self) -> tuple:
        pass

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
            user_list = {item['nick_name']: 0 for item in LeagueMember.objects.filter(league_name_id=key).values('nick_name')}
            if league_map[key] not in excluded_league_list:
                df_prediction = pd.DataFrame(PlayerPrediction[key], columns=cols)
                df_prediction['event_type'] = np.where(df_prediction['event_type'] == 'top_scorer', 'Top Scorer',
                                                   np.where(df_prediction['event_type'] == 'top_assist', 'Top Assist', None))
                new_cols = ['user_id', 'nick_name', 'event_type', 'player_name', 'count']
                df_merged = pd.merge(df_prediction, PlayerReal, on=['player_name', 'event_type'], how='inner')[new_cols]
                df_output = df_merged.groupby(['user_id', 'nick_name', 'event_type', 'player_name']).first().reset_index()
                elm_count = list(df_output['nick_name'].values)
                output[key] = {item: elm_count.count(item)*3 if item in list(set(elm_count)) else 0
                               for item in user_list}
            else:
                output[key] = user_list
        return output


class GetMatchData:
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
                  'home_team_id', 'home_team_score', 'away_team', 'away_team_id', 'away_team_score', 'match_label']
        return output, fields

    def current_live_game(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        output = df[df.match_status == '-1']
        if output.shape[0] > 1:
            return 'double'
        elif output.shape[0] == 1:
            return 'single'
        else:
            return 'zero'

    def next_match(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        output = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
        return output.head(1).reset_index()

    def prev_match(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        status = self.current_live_game()
        if status == 'double':
            output = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
            return output.head(2).tail(1).reset_index()
        else:
            output = df[df.match_status == '0'].sort_values(by=['match_date', 'match_hour'])
            return output.head(1).reset_index()

    def next_match_logos(self):
        teams_data = self.next_match()
        home = teams[teams_data.home_team[0]]['logo']
        away = teams[teams_data.away_team[0]]['logo']
        return {teams_data.home_team[0]: home, teams_data.away_team[0]: away}

    def prev_match_logos(self):
        teams_data = self.prev_match()
        home = teams[teams_data.home_team[0]]['logo']
        away = teams[teams_data.away_team[0]]['logo']
        return {teams_data.home_team[0]: home, teams_data.away_team[0]: away}

    def started_games(self) -> int:
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        games_played = int(df[df.match_status != '0'].shape[0])
        return games_played

    def top_players(self, event_type: int = 1) -> list:
        event_name = 'Top Scorer' if event_type == 1 else 'Top Assist'
        url = f'{self.PREFIX}/topplayers/40&apikey={self.TOKEN}&event_id={str(event_type)}&limit=1000'
        top_player_api = requests.get(url=url).json()['season']['players']
        top_player_list = [[item['shortname'], item['teamname'], int(item['eventCount']), f'{event_name}']
                           for item in top_player_api]
        top_player_list_adjusted = []
        for item in top_player_list:
            if [*item] == ['C. Ronaldo', 'Portugal', 1, 'Top Scorer']:
                top_player_list_adjusted.append(['C. Ronaldo', 'Portugal', 2, 'Top Scorer'])
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
                     title="Score Distribution",  labels={"score": "Score", "count": "Prediction Count", "winner": ""})
        fig.update_traces(textposition='inside')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT,)
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
        value = [1/(0.1 if item[2] == 0 else item[2]) for item in data]
        return {'source': source, 'target': target, 'value': value, 'label': label}

    @staticmethod
    def build_sankey_plot(data: dict) -> dict:
        link = dict(source=data['source'], target=data['target'], value=data['value'])
        node = dict(label=data['label'], pad=40, thickness=5)
        plot_data = go.Sankey(link=link, node=node)
        fig = go.Figure(plot_data)
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT,)
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    def top_players_pred_plot(self) -> dict:
        data = UserPredictionBase( user_id=self.user_id ).get_top_players_predictions()
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
            base_data = [[item[0]] + [*item[7:11]] for item in val if item[3] == match_label]
            df = pd.DataFrame(base_data, columns=['nick', 'p_h', 'p_a', 'r_h', 'r_a'])
            df['user_type'] = np.where(((df.p_h == df.r_h) & (df.p_a == df.r_a)), 'boomer',
                                       np.where(
                                            ((df.p_h > df.p_a) & (df.r_h > df.r_a)) |
                                            ((df.p_h == df.p_a) & (df.r_h == df.r_a)) |
                                            ((df.p_h < df.p_a) & (df.r_h < df.r_a))
                                            , 'winner', 'Loser'))
            adj_img_dict = {}
            relevant_users = [ids[i] for i in list(df[df.user_type != 'Loser']['nick'].unique())]
            for uid in relevant_users:
                adj_img_dict[uid] = f"{AWS_S3_URL}{images[uid]}" if uid in [i for i in images.keys()] else f"{AWS_S3_URL}{DEFAULT_PHOTO}"
            output[key] = {
                'Boomers': [[item, ids[item], adj_img_dict[ids[item]]] for item in df[df.user_type == 'boomer']['nick']],
                'Winners': [[item, ids[item], adj_img_dict[ids[item]]] for item in df[df.user_type == 'winner']['nick']]
            }
        return output

    def live_game_plot(self, match_label: str) -> dict:
        BaseClassData = UserPredictionBase(user_id=self.user_id)
        relevant_user_ids = BaseClassData.extract_relevant_user_ids()
        data = BaseClassData.present_predictions()[0]
        league_members_data = list(LeagueMember.objects.filter(user_name_id__in=relevant_user_ids).values('user_name_id', 'nick_name'))
        user_id_map = {item['nick_name']: item['user_name_id'] for item in league_members_data}
        unique_user_ids = list(set([item for item in user_id_map.values()]))
        user_image = {item['user_name_id']: item['header_image']
                      for item in list(UserImage.objects.filter(user_name_id__in=unique_user_ids).values())}
        output = {}
        for key, val in data.items():
            init_data = [[
                item[0],
                item[4],
                self.score_distance([int(i) for i in item[7:11]]),
                user_id_map[item[0]]
            ] for item in val if item[3] == match_label]
            relevant_data = [item for item in init_data if item[2] < 15]
            data_preps = self.data_sankey_live_game(relevant_data, league_name=key)
            output[key] = self.build_sankey_plot(data_preps)
        return output, self.get_live_winning_users(data, user_id_map, user_image, match_label)


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
                                          df.home_team, np.where(df.pred_score_home < df.pred_score_away, df.away_team, 'Draw'))
                df_winner = pd.DataFrame(df.groupby(['pred_dir'])['game_status'].count()).\
                    reset_index().rename(columns={
                        'game_status': 'count',
                        'pred_dir': 'winner'
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
                output[key] = obj
            return output
        else:
            return None

    @staticmethod
    def match_prediction_plot(data):
        fig = px.bar(data, x='score', y='count', color="winner", template='simple_white', text='count',
                     title="Score Distribution",  labels={"score": "Score", "count": "Prediction Count", "winner": ""})
        fig.update_traces(textposition='inside')
        fig.update_layout(font_family=vis.FAMILY_FONT, title_font_family=vis.FAMILY_FONT,)
        div = opy.plot(fig, auto_open=False, output_type='div')
        return div

    @staticmethod
    def match_winner_plot(data):
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

    def match_prediction_outputs(self):
        dict_score = self.match_prediction_df()
        dict_winner = self.match_winner_df()
        if dict_score is not None:
            output_score = {key: self.match_prediction_plot(data) for key, data in dict_score.items()}
            output_winner = {key: self.match_winner_plot(data) for key, data in dict_winner.items()}
            return self.merge_dicts(output_score, output_winner)
        else:
            return None






