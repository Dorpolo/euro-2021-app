# def all_matches(self):
#     data = self.extract_data()
#     # live_api_history = self.match_history_data()
#     # live_api_realtime = self.match_live_data()
#     live_api_history_matches = None  # [item for item in live_api_history.keys()]
#     live_api_realtime_matches = None  # [item for item in live_api_realtime.keys()] if live_api_realtime is not None else [ None]
#     live_fields = ['full_time_score', 'match_winner', '90min_home_team_score', '90min_away_team_score']
#     output = []
#     for item in data['calendar']['matchdays']:
#         match_day_id = item['matchdayID']
#         match_round = item['matchdayName']
#         match_day_playoff = item['matchdayPlayoff']
#         match_day_type = item['matchdayType']
#         match_day_start = item['matchdayStart']
#         match_day_end = item['matchdayEnd']
#         for subitem in item['matches']:
#             match_id = subitem['matchID']
#             match_status = subitem['matchStatus']['statusID']
#             match_date = subitem['matchDate']
#             match_hour = subitem['matchTime']
#             home_team = subitem['homeParticipant']['participantName']
#             home_team_id = subitem['homeParticipant']['participantID']
#             home_team_score = subitem['homeParticipant']['score']
#             away_team = subitem['awayParticipant']['participantName']
#             away_team_id = subitem['awayParticipant']['participantID']
#             away_team_score = subitem['awayParticipant']['score']
#             match_label = f"{home_team}-{away_team}"
#             row = [match_day_id, match_round, match_day_playoff, match_day_type, match_day_start,
#                    match_day_end, match_id, match_status, match_date, match_hour, home_team, home_team_id,
#                    home_team_score, away_team, away_team_id, away_team_score, match_label
#                    ]
#             # if match_label in live_api_realtime_matches:
#             #     extra_data = [live_api_realtime[match_label][item] for item in live_fields]
#             # elif match_label in live_api_history_matches:
#             #     extra_data = [live_api_history[match_label][item] for item in live_fields]
#             #     row += extra_data + [True]
#             # else:
#             #     row += [None for item in live_fields] + [False]
#             output.append(row)
#     fields = ['match_day_id', 'match_round', 'match_day_playoff', 'match_day_type', 'match_day_start',
#               'match_day_end', 'match_id', 'match_status', 'match_date', 'match_hour', 'home_team',
#               'home_team_id', 'home_team_score', 'away_team', 'away_team_id', 'away_team_score', 'match_label',
#               # 'live_ft_score', 'live_match_winner', 'live_90_home_score', 'live_90_away_score', 'is_enriched'
#               ]
#     return output, fields


# class LiveGameViewOld:
#     def next(request):
#         is_next = True
#         match_router = GetMatchData().game_router()
#         match = match_router['next']['data'] if is_next else match_router['prev']['data']
#         status = match['match_status']
#         real_winner = match['away_team'] if match['match_winner'] == 'away' else match['home_team'] if match['match_winner'] == 'home' else 'Draw'
#         onboarding = BaseViewUserControl(request.user.id).onboarding()
#         if onboarding['bet']:
#             LiveOutput = TopPlayerStats(request.user.id).live_game_plot(match_label=match['match_label'])
#         else:
#             LiveOutput = [None, None]
#         context = {
#             'title': match['match_label'],
#             'real_score': f"{int(match['home_score_90_min'])}-{int(match['away_score_90_min'])} ({real_winner})",
#             'status': 'Fixture' if status == '0' else 'Started' if status == '-1' else 'Finished',
#             'plots': LiveOutput[0],
#             'logos': match_router['next']['logo'] if is_next else match_router['prev']['logo'],
#             'entitled_users': LiveOutput[1],
#             'committed_a_bet': onboarding['bet'],
#         }
#         template_name = f"stats_live_game_{'next' if is_next else 'prev'}.html"
#         return render(request, template_name, context)
#
#     def prev(request):
#         is_next = False
#         match_router = GetMatchData().game_router()
#         match = match_router['next']['data'] if is_next else match_router['prev']['data']
#         status = match['match_status']
#         real_winner = match['away_team'] if match['match_winner'] == 'away' else match['home_team'] if match['match_winner'] == 'home' else 'Draw'
#         onboarding = BaseViewUserControl(request.user.id).onboarding()
#         if onboarding['bet']:
#             LiveOutput = TopPlayerStats(request.user.id).live_game_plot(match_label=match['match_label'])
#         context = {
#             'title': match['match_label'],
#             'real_score': f"{int(match['home_score_90_min'])}-{int(match['away_score_90_min'])} ({real_winner})",
#             'status': 'Fixture' if status == '0' else 'Started' if status == '-1' else 'Finished',
#             'plots': LiveOutput[0],
#             'logos': match_router['next']['logo'] if is_next else match_router['prev']['logo'],
#             'entitled_users': LiveOutput[1],
#             'committed_a_bet': onboarding['bet'],
#         }
#         template_name = f"stats_live_game_{'next' if is_next else 'prev'}.html"
#         return render(request, template_name, context)
#
# class MyPredictionsView1(TemplateView):
#     template_name = "my_predictions.html"
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             UserPred = UserPredictionBase(request.user.id)
#             get_my_predictions = UserPred.present_my_predictions()
#             for row in get_my_predictions[0]:
#                 home, away = row[3].split('-')
#                 winner_label = '' if row[6] == 'Fixture' else home if row[15] == 'home' else away if row[
#                                                                                                          15] == 'away' else 'Draw'
#                 row[15] = winner_label
#                 if 'Final' not in row[12]:
#                     row[17], row[19] = row[9], row[9]
#                     row[18], row[20] = row[10], row[10]
#             get_my_players = UserPred.get_top_players_my_predictions()
#         else:
#             get_my_predictions = None
#         context = {
#             'my_predictions': get_my_predictions[0],
#             'my_players': get_my_players
#         }
#         return render(request, self.template_name, context)



# class AllPredictionsView1(TemplateView):
#     template_name = "score_predictions.html"
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             UserPrediction = UserPredictionBase(request.user.id)
#             get_league_data = UserPrediction.present_predictions()
#             league_data_output = get_league_data[0]
#             for league_data in league_data_output.values():
#                 for row in league_data:
#                     home, away = row[3].split('-')
#                     winner_label = '' if row[6] == 'Fixture' else home if row[15] == 'home' else away if row[15] == 'away' else 'Draw'
#                     row[15] = winner_label
#                     if 'Final' not in row[12]:
#                         row[17], row[19] = row[9], row[9]
#                         row[18], row[20] = row[10], row[10]
#             league_table_output = UserPrediction.league_member_points()
#         else:
#             league_data_output = None
#         onboarding = BaseViewUserControl(request.user.id).onboarding()
#         context = {
#             'league_members': league_data_output,
#             'league_signup': onboarding['league'],
#             'committed_a_bet': onboarding['bet'],
#             'image_uploaded': onboarding['image'],
#             'committed_a_bet_16': onboarding['bet_top_16'],
#             'committed_a_bet_8': onboarding['bet_top_8'],
#             'committed_a_bet_4': onboarding['bet_top_4'],
#             'committed_a_bet_2': onboarding['bet_top_2'],
#             'league_member_points': league_table_output
#         }
#         return render(request, self.template_name, context)


# class HomeView(TemplateView):
#     template_name = "home.html"
#     GetAPIData = GetMatchData()
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             UserPred = UserPredictionBase(request.user.id)
#             onboarding = BaseViewUserControl(request.user.id).onboarding()
#             league_data_output = UserPred.get_league_members()
#             home_page_context = self.GetAPIData.game_router()
#             if league_data_output is not None:
#                 context = {
#                     'show_results': False,  # TODO - change to True once bet window ends
#                     'league_members': league_data_output,
#                     'league_signup': onboarding['league'],
#                     'committed_a_bet': onboarding['bet'],
#                     'image_uploaded': onboarding['image'],
#                     'committed_a_bet_16': onboarding['bet_top_16'],
#                     'committed_a_bet_8': onboarding['bet_top_8'],
#                     'committed_a_bet_4': onboarding['bet_top_4'],
#                     'committed_a_bet_2': onboarding['bet_top_2'],
#                     'is_cup_user': UserPred.is_cup_user(),
#                     'prev_match_logos': home_page_context['prev']['logo'],
#                     'next_match_logos': home_page_context['next']['logo'],
#                 }
#                 if onboarding['bet']:
#                     presented_data = UserPred.home_screen_match_relevant_data(home_page_context)
#                     context['user_game_points'] = presented_data[2]
#                     context['next_match'] = presented_data[1]
#                     context['prev_match'] = presented_data[0]
#                     context['league_member_points'] = UserPred.league_member_points()
#                     context['league_memberships'] = UserPred.get_league_members_data()
#                     context['games_started'] = home_page_context['started_games']
#                     context['bet_id'] = UserPred.user_game_bet_id('group')
#                     context['bet_id_knockout'] = UserPred.user_game_bet_id('top_16')
#                     context['bet_id_knockout_8'] = UserPred.user_game_bet_id('top_8')
#                 return render(request, self.template_name, context)
#             else:
#                 return render(request, self.template_name, {'data': None})
#         else:
#             return render(request, self.template_name, {'data': None})

# path('home/', views.HomeView().get, name='better_home'),