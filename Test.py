import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY = os.environ['STEAM_API_KEY']
STEAM_USER_ID = os.environ['STEAM_USER_ID']

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
        for game in owned_games:
            print(f"- {game['name']}")
    else:
        print("No games found in the library.")