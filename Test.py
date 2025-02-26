import requests
import json
import os
from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
import polars as pl
from SQL_Create_Connection_String import engine

load_dotenv()

STEAM_API_KEY = os.environ['STEAM_API_KEY']
STEAM_USER_ID = os.environ['STEAM_USER_ID']

def get_how_long_to_beat():
    url = "https://api.npms.io/v2/package/howlongtobeat"
    response = requests.get(url)
    if response.status_code == 200:
        #print("Sucessfully requested howlongtobeat")
        return response.json()['response'].get('Nioh', [])
    else:
        print(f"Error: {response.status_code}")
        return []

def get_owned_games(steam_id, api_key):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json&include_appinfo=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['response'].get('games', [])
    else:
        print(f"Error: {response.status_code}")
        return []

if __name__ == "__main__":
    owned_games = get_owned_games(STEAM_USER_ID, STEAM_API_KEY)
    if owned_games:
        owned_games_df = pl.DataFrame(None,
                           schema=
                           {
                               "game_name": pl.String,
                               "hltb_game_name": pl.String,
                               "completionist_time": pl.Float64,
                               "found": pl.Boolean,
                               "same": pl.Boolean
                           })
        game_name = 'TEMP VALUE'
        completion_time = 0.0
        print("There are " + str(len(owned_games)) + " games in your Steam library.")
        for i, game in enumerate(owned_games):
            result_list = HowLongToBeat().search(game['name'])
            if result_list is not None and len(result_list) > 0:
                #make sure its from steam too
                best_element = max(result_list, key=lambda element: element.similarity)
                print(str(i) + ": " + best_element.game_name + " loaded")
                game_name = best_element.game_name
                completion_time = best_element.completionist
                found_bool = True
            else:
                print(str(i) + ": " + game['name'] + " not loaded")
                game_name = 'TEMP VALUE'
                completion_time = 0.0
                found_bool = False

            if game['name'] == game_name:
                same_bool = True
            else:
                print(game['name'] + " is different than " + game_name)
                same_bool = False
            new_row = \
                {
                    "game_name": game['name'],
                    "hltb_game_name": game_name,
                    "completionist_time": completion_time,
                    "found": found_bool,
                    "same": same_bool


                }
            df_new_row = pl.DataFrame(new_row)
            owned_games_df = owned_games_df.vstack(df_new_row)



            #print(f"- {game['name']}")
    else:
        print("No games found in the library.")


    insert_df = owned_games_df.filter(pl.col("found") is True)
    insert_df = insert_df.filter(pl.col("same") is True)
    insert_df = insert_df.drop("hltb_game_name")
    insert_df = insert_df.drop("found")
    insert_df = insert_df.drop("same")
    insert_df.write_database(table_name="games.owned_games_list", connection=engine)
