def all_matches(self):
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