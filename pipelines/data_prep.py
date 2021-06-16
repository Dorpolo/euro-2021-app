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

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(SECRET_KEY=str,)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


class MailTemplate:
    def prepare_bet_submission_email(request, form) -> dict:
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

    def prepare_league_user_email(request, form) -> dict:
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
        bet_data = Game.objects.filter(user_name_id=self.user_id)
        image = UserImage.objects.filter(user_name_id=self.user_id)
        league_assigned = True if len(league_data) > 0 else False
        bet_assigned = True if len(bet_data) > 0 else False
        image_uploaded = True if len(image) > 0 else False
        return {'league': league_assigned, 'bet': bet_assigned, 'image': image_uploaded}


class UserPredictionBase:
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

    def get_user_leagues(self) -> tuple:
        league_member_data = list(LeagueMember.objects.filter(user_name_id=self.user_id).values())
        leagues = [item['league_name_id'] for item in league_member_data]
        if len(leagues) > 0:
            return True, leagues
        else:
            return False, None

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

    def get_user_prediction(self):
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
        df_real_players = TopPlayerStats( self.user_id ).top_players_real()
        df_output = pd.merge(df_predictions, df_real_players[1], on=['player_name', 'event_type'], how='left')
        output = {item: df_output[df_output.event_type == item][['player_name', 'team', 'count']].values.tolist()
                  for item in ['Top Scorer', 'Top Assist']}
        return output

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

    def present_predictions(self) -> tuple:
        data = self.data_enrichment()
        leagues = list(data[data.user_name_id == self.user_id]['league_name_id'].unique())
        if len(leagues) > 0:
            output = {}
            required_fields = ['nick_name', 'date', 'hour', 'match_label', 'predicted_score', 'real_score',
                               'game_status', 'pred_score_home', 'pred_score_away', 'real_score_home',
                               'real_score_away', 'user_name_id']
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
                               'real_score_away', 'user_name_id']
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
        x['is_direction'] = np.where(x.pred_dir == x.real_dir, 1, 0)
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
        init_match = GetMatchData()
        next_match_df = init_match.next_match()
        prev_match_df = init_match.prev_match()
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

    def user_current_prediction(self):
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
                filtered_df['status_rank'] = np.where(filtered_df.game_status == 'Finished', 1, 0)
                final_df = filtered_df.sort_values(by=['status_rank', 'date', 'hour']).drop(columns='status_rank')
                output[item] = final_df.values.tolist()
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
            int((x['started'] * x['is_boom']).sum()),
            int((x['started'] * x['is_direction']).sum()),
            round((x['started'] * x['points']).sum()*100/(x['started'] * 3).sum(), 1),
            int((x['started'] * x['is_boom'] * (x['pred_score_home'].astype(int) + x['pred_score_away'].astype(int))).sum()),
            int((x['is_live'] * x['points']).sum()),
        ]
        index_names = ['games', 'points', 'boom', 'direction', 'success_rate', 'predicted_goals', 'live_points']
        return pd.Series(d, index=[index_names])

    @staticmethod
    def adjust_table_column_type(data) -> list:
        adj_df = []
        for item in data.values.tolist():
            nick = [item[0]]
            values = [int(sub) for sub in item[1:]]
            values[4] = f"{values[4]}%"
            adj_df.append(nick + values)
        return adj_df

    def get_game_points_group_stage(self, df):
        data = df.groupby(['user_name_id', 'nick_name']).apply(self.table_calculations).\
            reset_index().sort_values(
                    by=[('points',), ('boom',), ('direction', ), ('predicted_goals', )], ascending=[False]*4
                    )[['nick_name', 'games', 'points', 'boom', 'direction', 'success_rate',
                       'predicted_goals', 'live_points', 'user_name_id']]
        data['rn'] = np.arange(len(data)) + 1
        return self.adjust_table_column_type(data)

    def get_user_league_rank(self) -> dict:
        get_user_points = self.league_member_points()
        print(get_user_points)
        return {key: {sub[0]: sub[9] for sub in val} for key, val in get_user_points.items()}

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

    def next_match(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        output = df[df.match_status != '1'].sort_values(by=['match_date', 'match_hour'])
        return output.head(1).reset_index()

    def prev_match(self):
        df_input = self.all_matches()
        df = pd.DataFrame(df_input[0], columns=df_input[1])
        output = df[df.match_status == '1'].sort_values(by=['match_date', 'match_hour'])
        return output.tail(1).reset_index()

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
        return top_player_list


class TopPlayerStats(GetMatchData):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def top_players_real(self) -> tuple:
        scorers = self.top_players(1)
        assists = self.top_players(2)
        players_dict = {'top_scorer': scorers, 'top_assists': assists}
        cols = ['player_name', 'team', 'count', 'event_type']
        df = pd.DataFrame(scorers + assists, columns=cols)
        return players_dict, df

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






