import requests
import json
import os
from dotenv import load_dotenv
from howlongtobeatpy import HowLongToBeat
import polars as pl


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
        print("Games in your Steam library:")
        owned_games_df = pl.DataFrame(None,
                           schema={"actual_game_name": pl.String, "game_name": pl.String, "completionist_time": pl.Float64})


        for i, game in enumerate(owned_games):
            result_list = HowLongToBeat().search(game['name'])
            if result_list is not None and len(result_list) > 0:
                best_element = max(result_list, key=lambda element: element.similarity)
                new_row = \
                {
                    "actual_game_name": game['name'],
                    "game_name": best_element.game_name,
                    "completionist_time": best_element.completionist
                }
                df_new_row = pl.DataFrame(new_row)
                owned_games_df = owned_games_df.vstack(df_new_row)
                print(game['name'] + " " + best_element.game_name + " loaded")


            #print(f"- {game['name']}")
    else:
        print("No games found in the library.")

    test = 0