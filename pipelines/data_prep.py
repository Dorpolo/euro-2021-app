from data.teams import team_game_map
from myapp.models import Game, League, LeagueUser
import plotly.graph_objects as go
import numpy as np


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
    data = LeagueUser.objects.filter(user_name_id=user)
    return data[0].email


def extract_user_league_name_id(user) -> tuple:
    data = LeagueUser.objects.filter(user_name_id=user)
    if len(data) > 0:
        league_name_id = data[0].league_name_id
        return True, league_name_id
    else:
        return False, None


def extract_league_users(user) -> tuple:
    l_name_id = extract_user_league_name_id(user)
    if l_name_id[0]:
        data = LeagueUser.objects.filter(league_name_id=l_name_id[1])
        user_list = {item.user_name_id:
                         {'first_name': item.first_name,
                          'last_name': item.last_name
                          } for item in data}
        return True, user_list
    else:
        return False, None


def extract_league_bets(user):
    league_users = extract_league_users(user)
    if league_users[0]:
        unique_users = [item for item in league_users[1].keys()]
        data = list(Game.objects.all().values())
        filtered_data = [item for item in data if item['user_name_id'] in unique_users]
        return filtered_data
    else:
        return None


def user_onboarding(user) -> dict:
    league_data = LeagueUser.objects.filter(user_name_id=user)
    bet_data = Game.objects.filter(user_name_id=user)
    league_assigned = True if len(league_data) > 0 else False
    bet_assigned = True if len(bet_data) > 0 else False
    return {'league': league_assigned, 'bet': bet_assigned}


def user_game_bet_id(user) -> dict:
    data = Game.objects.filter(user_name_id=user)
    if len(data) > 0:
        return data[0].id
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





