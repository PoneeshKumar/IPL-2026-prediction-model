import pandas as pd
import numpy as np
from pathlib import Path
import json


"Load ball by ball data from the JSON files and return it as a pandas DataFrame."
def load_ball_by_ball(path):

    raw_path = Path(path)
    all_deliveries = []

    for file_path in raw_path.glob('*.json'):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {file_path}")
                continue

            info = data.get('info', {})
            match_id = file_path.stem
            teams = info.get('teams', [None, None])
            date = info.get('dates', [None])[0]
            season = info.get('season')
            winner = info.get('outcome', {}).get('winner')

            # for each innings get pertinient data
            for innings in data.get('innings', []):
                inning_number = innings.get('1st innings') or innings.get('2nd innings') or innings.get('3rd innings') or innings.get('4th innings')
                if inning_number is None:
                    continue

                for delivery in inning_number.get('deliveries', []):
                    batting_team = inning_number.get('team')
                    bowling_team = teams[0] if teams[1] == batting_team else teams[1]

                    for over in innings.get('overs', []):
                        over_number = over.get('over')
                        for delivery in over.get('deliveries', []):
                            delivery_number = delivery.get('delivery')
                            batsman = delivery.get('batter')
                            bowler = delivery.get('bowler')
                            runs = delivery.get('runs', {}).get('total', 0)
                            extras = delivery.get('runs', {}).get('extras', 0)
                            total_runs = runs + extras
                            wicket = delivery.get('wicket', {})
                            is_wicket = 1 if wicket else 0
                            dismissal_kind = wicket.get('kind') if wicket else None
                            player_out = wicket.get('player_out') if wicket else None

                            all_deliveries.append({
                                "match_id": match_id,
                                "season": season,
                                "date": pd.to_datetime(date),
                                "batting_team": batting_team,
                                "bowling_team": bowling_team,
                                "venue": info.get("venue"),
                                "over": over_num,
                                "batter": delivery.get("batter"),
                                "bowler": delivery.get("bowler"),
                                "runs_off_bat": runs.get("batter", 0),
                                "extras": runs.get("extras", 0),
                                "total_runs": runs.get("total", 0),
                                "is_wicket": int(len(wickets) > 0),
                                "winner": winner,
                            })

        return pd.DataFrame(all_deliveries)

"compute team level features from each mathch and return a DataFrame with one row per match and team"
"This function computes team-level features from the matches DataFrame. It calculates total runs scored, total wickets taken, and average runs per over for each team in each match. The resulting DataFrame has one row per match and team, with columns for match_id, team, total_runs, total_wickets, and average_runs_per_over."
"only use data from before the match to compute the features, so that we don't leak information from the future"
def compute_team_features(matches_df):
    matches_df = matches_df.sort_values("date").reset_index(drop=True)
    features_row = []

    for idx, match in matches_df.iterrows():
        past = matches_df[matches_df["date"] < match["date"]]
        t1, t2 = match["team1"], match["team2"]
        venue = match["venue"]

        def win_rate(team, df, window=10): 
            team_matches = df[(df["team1"] == team) | (df["team2"] == team)].tail(window)
            if len(team_matches) == 0:
                return 0.5
        return (team_matches["winner"] == team).mean()
    
        def hsh_win_rate(team, opponent, df):
            h2h = df[
                ((df["team1"] == team) & (df["team2"] == opponent)) |
                ((df["team1"] == opponent) & (df["team2"] == team))
            ]
            if len(h2h) == 0:
                return 0.5
            return (h2h["winner"] == team).mean()
        
        def venue_win_rate(team, venue, df):
            at_venue = df[
                ((df["team1"] == team) | (df["team2"] == team)) &
                (df["venue"] == v)
            ]
            if len(at_venue) == 0:
                return 0.5
            return (at_venue["winner"] == team).mean()

        def toss_advantage(team, v, decision, df):
            subset = df[
                (df["toss_winner"] == team) &
                (df["toss_decision"] == decision) &
                (df["venue"] == v)
            ]
            if len(subset) == 0:
                return 0.5
            
            return (subset["winner"] == team).mean()

        toss_win = match["toss_winner"]
        toss_dec = match["toss_decision"]
        feature_rows.append({
            "match_id": match["match_id"],
            "date": match["date"],
            "season": match["season"],
            "team1": t1,
            "team2": t2,
            "venue": venue,
            # Form features
            "team1_form_5": win_rate(t1, past, 5),
            "team1_form_10": win_rate(t1, past, 10),
            "team2_form_5": win_rate(t2, past, 5),
            "team2_form_10": win_rate(t2, past, 10),
            # Head-to-head
            "h2h_team1_winrate": h2h_win_rate(t1, t2, past),
            # Venue
            "team1_venue_winrate": venue_win_rate(t1, venue, past),
            "team2_venue_winrate": venue_win_rate(t2, venue, past),
            # Toss
            "toss_winner_is_team1": int(toss_win == t1),
            "toss_decision": toss_dec,
            "team1_toss_venue_winrate": toss_advantage(t1, venue, toss_dec, past),
            # Target
            "team1_wins": int(match["winner"] == t1),
        })

    return pd.DataFrame(feature_rows)




