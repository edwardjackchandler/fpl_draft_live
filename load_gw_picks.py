from fpl import draft
import pandas as pd
import logging

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

game_weeks = [ i for i in range(1, 39) ]
game_week_api = draft.ApiScraper(41747, 38)

# Player Stats
# print(game_week_api.get_player_stats())
print(game_week_api.get_named_player_stats().head(5))

df = 
bucket = 
folders
file_name
game_week_api.df_parquet_write_s3()
's3://bucket/folder/bucket.parquet.gzip'

# Pick Details
#print(game_week_api.get_league_pick_details())
# league_pick_details = game_week_api.get_league_pick_details()
# print(league_pick_details.shape)
# print(league_pick_details)

# for game_week in game_weeks:
#     game_week_details = draft.ApiScraper(41747, game_week)
#     print(game_week_details.get_team_score())