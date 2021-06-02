from datetime import date, datetime
from pandas.core.reshape.concat import concat
import requests
import pandas as pd
import logging
from functools import reduce

# serverless deploy -v
# serverless invoke -f fpl_live_score -l
# League = 41747

class ApiScraper():
    def __init__(self, league, game_week):
        self.game_week = game_week
        self.fixtures_url = f"https://fantasy.premierleague.com/api/fixtures/?event={game_week}"
        self.team_url = f"https://draft.premierleague.com/api/entry/{{entry_id}}/event/{game_week}"
        self.live_players_url = f"https://draft.premierleague.com/api/event/{game_week}/live"
        self.league_details_url = f"https://draft.premierleague.com/api/league/{league}/details"
        self.player_details_url = "https://draft.premierleague.com/api/bootstrap-static"

    def get_live_scores_call(self):
        return { k: v for k, v in sorted(self.get_live_scores_json().items(), key=lambda item: item[1], reverse=True) }

    def get_live_scores_json(self):
        return { pair[0]: pair[1] for pair in self.get_live_scores().values()}
    
    def get_live_scores(self):
        teams_dict = { 
            manager_dict["entry_id"]: (manager_dict["entry_name"], int(self.get_ordered_team_score(manager_dict["entry_id"])))
            for manager_dict in self.get_league_entries()
        }

        return teams_dict
        
    def get_league_pick_details(self):
        managers_pdf = self.get_league_entries_pdf()
        entry_ids = managers_pdf['entry_id'].tolist()
        manager_pick_details = []

        for entry_id in entry_ids:
            manager_pick_details.append(self.get_pick_details(entry_id))

        manager_pick_details_pdf = pd.concat(manager_pick_details)

        return manager_pick_details_pdf.merge(
            managers_pdf,
            on='entry_id'
        )

    def get_live_score_pdf(self):  
        teams = pd.DataFrame(requests_json_return(self.league_details_url)["standings"])
        live_scores = pd.DataFrame(requests_json_return(self.league_details_url)["league_entries"])
        scores = teams.merge(live_scores, left_on="league_entry", right_on="id")

        scores["live_scores"] = scores["entry_id"].apply(self.get_ordered_team_score)
        scores["live_total"] = scores["live_scores"] - scores["event_total"] + scores["total"]
        scores = scores.reset_index()
        scores["rank"] = scores["index"] + 1

        # Add URL to the team
        scores["entry_name_with_link"] = scores.apply(lambda x: self._add_link_to_name(x.entry_id, x.entry_name), axis=1)

        return scores

    def get_live_score_pdf_formatted(self):
        scores = self.get_live_score_pdf()
        scores["full_name"] = scores["player_first_name"] + " " + scores["player_last_name"]

        cols = [
            "rank",
            "entry_name",
            "entry_name_with_link",
            "full_name",
            "live_scores",
            "live_total"
        ]
        rename = [
            "Rank",
            "Team Name",
            "Team Link",
            "Player Name",
            "GW Score",
            "Total Score"
        ]

        scores = scores[cols]
        scores.columns = rename
        return scores.sort_values(["Total Score"], ascending=False)

    def _add_link_to_name(self, entry_id, team_name):
        return 'https://draft.premierleague.com/entry/{entry_id}/event/{game_week}'\
            .format(entry_id=entry_id, game_week=self.game_week)

    def get_league_entries(self):
        return requests_json_return(self.league_details_url)["league_entries"]

    def get_league_entries_pdf(self):
        return pd.DataFrame(self.get_league_entries())

    def get_picks(self, entry_id):
        team_url = self.team_url.format(entry_id=entry_id)
        json = requests_json_return(team_url)

        return pd.DataFrame(json["picks"])

    def get_pick_details(self, entry_id):
        picks_pdf = self.get_picks(entry_id)
        player_stats_pdf = self.get_live_player_stats()

        pick_details = picks_pdf.merge(
            player_stats_pdf, 
            left_on="element", 
            right_on="index"
        )

        pick_details['entry_id'] = entry_id

        return pick_details

    def get_ordered_team_score(self, entry_id):
        return self.get_live_score(self.get_pick_details(entry_id), self.fixtures_url)

    def get_live_player_stats(self):
        json = requests_json_return(self.live_players_url)

        live_players_pdf = pd.DataFrame({ 
            k:v["stats"] for k, v in json["elements"].items() 
        }).transpose().reset_index().apply(pd.to_numeric)
        live_players_pdf['id'] = live_players_pdf['index']
        return live_players_pdf.drop('index', axis=1)

    def get_player_stats(self):
        player_stats = pd.DataFrame(
            requests_json_return(self.player_details_url)["elements"]
        )
        element_types = pd.DataFrame(
            requests_json_return(self.player_details_url)["element_types"]
        )

        # these columns come up in the player_stats and live_player dataframes
        # so we need to add a total_ prefix to be able to differentiate
        total_columns = [
            'minutes', 'goals_scored', 'assists', 'clean_sheets',
            'goals_conceded', 'own_goals', 'penalties_saved',
            'penalties_missed', 'yellow_cards', 'red_cards', 'saves',
            'bonus', 'bps', 'influence', 'creativity', 'threat',
            'ict_index', 'total_points', 'in_dreamteam'
        ]

        for col in total_columns:
            player_stats = player_stats.rename(columns={col: 'total_' + col})

        return player_stats.merge(
            element_types,
            on='id',
            how='left'
        )

    def get_football_teams(self):
        return pd.DataFrame(
            requests_json_return(self.player_details_url)["teams"]
        )

    def get_named_player_stats(self):
        return self.get_live_player_stats().merge(
            self.get_player_stats(),
            on='id',
            how='left'
        )

    def get_gw_fixture_times(self, url):
        json = requests_json_return(url)
        return { fixture_dict["code"]:fixture_dict["kickoff_time"] for fixture_dict in json }
        
    def get_last_day(self, fixtures_url):
        get_times = self.get_gw_fixture_times(fixtures_url)
        return list(get_times.values())[-1]

    def which_onfield_subs_play(self, live_player_scores):
        # assume that it's the last game
        # everyone that can have minutes played, should have minutes played at this point
        total_player_count = live_player_scores[live_player_scores["minutes"] > 0]["minutes"].count()

        if total_player_count >= 11:
            return 0
        elif total_player_count == 10:
            return 1
        elif total_player_count == 9:
            return 2
        else:
            return 3

    def which_gk_subs_play(self, live_player_scores):
        # assume that it's the last game
        # everyone that can have minutes played, should have minutes played at this point
        if live_player_scores[live_player_scores["position"] == 1]["minutes"].sum() > 0:
            return False
        else:
            return True

    def get_live_score(self, live_player_scores, fixtures_url):
        bench_goal_keeper = 12
        full_bench = [12, 13, 14, 15]

        team_without_subs = live_player_scores[~live_player_scores["position"].isin(full_bench)]
        team_with_no_gk_sub = live_player_scores[~live_player_scores["position"].isin([bench_goal_keeper])]
        gk_sub = live_player_scores[live_player_scores["position"].isin([bench_goal_keeper])]
        
        gw_last_datetime = datetime.strptime(self.get_last_day(fixtures_url), "%Y-%m-%dT%H:%M:%SZ")

        if datetime.now() < gw_last_datetime:
            return team_without_subs["total_points"].sum()
        else:
            live_scores_with_subs = team_with_no_gk_sub[0:11+self.which_onfield_subs_play(team_without_subs)]
            
            if self.which_gk_subs_play(live_player_scores):
                live_scores_with_subs = pd.concat([live_scores_with_subs, gk_sub])
            
            return live_scores_with_subs["total_points"].sum()

    def get_total_scores(self):
        return pd.DataFrame(requests_json_return(self.league_details_url)["standings"])

    def df_parquet_write_s3(self, bucket, folders, file_name, df, partition_cols=None):
        full_path = 's3://' + bucket + folders + str(self.game_week) + '/' + file_name
        df.to_parquet(full_path, compression=None, partition_cols=partition_cols)
        print(df.head(5))
        logging.warning("Loading dataframe into {full_path}".format(full_path=full_path))


def requests_json_return(url):
    logging.warning(f'Pulling data from {url} Draft FPL API')
    r = requests.get(url)
    logging.warning('Data Loaded into Memory')
    return r.json()


class S3Writer():
    def df_parquet_write_s3(self, bucket, folders, file_name, game_week, df):
        full_path = 's3://' + bucket + folders + game_week + '/' + file_name + 'parquet.gzip'
        df.to_parquet(full_path, compression='gzip', partition_cols=['game_week'])

# 1. Create a function that loads the GW document from the API (/)
# 2. Create a function that cleans the GW document and puts it into a tabular format (/)
# 3. Create a function that load the GW into parquet
# 4. Create a function that sends the parquet file to S3