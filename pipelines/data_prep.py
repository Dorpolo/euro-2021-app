from data.teams import team_game_map
from myapp.models import Game, League, LeagueMember, UserImage
import plotly.graph_objects as go
import numpy as np
from myproject.settings import MEDIA_URL, AWS_S3_URL, DEFAULT_PHOTO
from collections import defaultdict

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
        unique_leagues = [item for item in league_users[1].keys()]
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


