from fpl import draft
import pandas as pd
import logging

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

game_weeks = [ i for i in range(1, 39) ]

y = False
if y == True:
    game_week = 1
    game_week_details = draft.ApiScraper(41747, game_week)
    df = game_week_details.get_league_pick_details()

    print(df.columns)
    bucket = 'last-draft/'
    folders = 'draft_data/'
    file_name = 'named_player_stats.parquet'
#game_week_api.df_parquet_write_s3(bucket, folders, file_name, df)

# x = pd.read_parquet('s3://last-draft/draft_data/38/named_player_stats.parquet')
# print(x.head(5))
# 's3://bucket/folder/bucket.parquet.gzip'

# Pick Details
# print(game_week_api.get_league_pick_details())
# league_pick_details = game_week_api.get_league_pick_details()
# print(league_pick_details.shape)
# print(league_pick_details)

df_list = []
x = True
if x == True:

    for game_week in game_weeks:
        print("game_week", game_week)
        game_week_details = draft.ApiScraper(41747, game_week)
        df = game_week_details.get_league_pick_details()
        df['game_week'] = game_week
        df_list.append(df)

    total_data = pd.concat(df_list)
    total_data.to_csv("league_pick_details.csv", index=False)
    #print(total_data.head(5))