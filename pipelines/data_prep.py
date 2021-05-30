from data.teams import team_game_map
from myapp.models import Game, League, LeagueUser, Post


def prepare_bet_submission_email(request, form) -> dict:
    home = []
    away = []
    results = []
    for i in enumerate(form.cleaned_data.items()):
        if i[0] % 2 == 0:
            home.append(i[1])
        else:
            away.append(i[1])
    for h, a in zip(home, away):
        result = f"{team_game_map[h[0]]}-{team_game_map[a[0]]}: {h[1]}-{a[1]}"
        results.append(result)
    text_results = '\n'.join(results)
    subject = "Euro 2021 Friends League - Email Confirmation - Bet Submission"
    message = f"Dear {request.user.username}!\n" \
              f"You have just submitted successfully your bet form!\n" \
              f"Please Note - you can easily edit your bets by 2021-07-09 at 11:59:59 PM using the app 'edit your bet' tab.\n\n" \
              f"For your convenience and our documentation, please find bellow your bets. Please note " \
              f"that every change you will made, a new email will be sent with your most updated bets.\n\n" \
              f"{text_results}\n\n" \
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


def extract_user_league_name_id(user) -> str:
    data = LeagueUser.objects.filter(user_name_id=user)
    league_name_id = data[0].league_name_id
    return league_name_id


def extract_league_users(user) -> dict:
    l_name_id = extract_user_league_name_id(user)
    data = LeagueUser.objects.filter(league_name_id=l_name_id)
    user_list = {item.user_name_id:
                     {'first_name': item.first_name,
                      'last_name': item.last_name
                      } for item in data}
    return user_list


def extract_league_bets(user) -> dict:
    league_users = extract_league_users(user)
    unique_users = [item for item in league_users.keys()]
    data = list(Game.objects.all().values())
    filtered_data = [item for item in data if item['user_name_id'] in unique_users]
    return filtered_data





