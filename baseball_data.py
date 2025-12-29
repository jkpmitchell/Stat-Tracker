# MLB player data will be used for analysis and modeling in this project using thier API.
# The use of their API is free for non-commercial purposes, which will allow for key not to be used.

import requests
import pandas as pd
from datetime import datetime, timedelta
import config

def search_player(name):
    """Find a player by name"""
    url = f"{config.MLB_API_URL}/people/search"
    params = {"names": name, "sportId": 1}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    players = []
    for person in data.get('people', []):
        players.append({
            'id': person['id'],
            'name': person['fullName'],
            'team': person.get('currentTeam', {}).get('name', 'Free Agent')
        })
    return players

def get_player_stats(player_id, days=30):
    """Get recent stats for a player"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    url = f"{config.MLB_API_URL}/people/{player_id}/stats"
    params = {
        "stats": "gameLog",
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d")
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    games = []
    if data.get('stats') and data['stats'][0].get('splits'):
        for game in data['stats'][0]['splits']:
            game_stats = game['stat']
            game_stats['date'] = game['date']
            game_stats['player_name'] = game.get('player', {}).get('fullName', 'Unknown')
            games.append(game_stats)
    
    return pd.DataFrame(games)

def save_data(df, filename):
    """Save data to CSV"""
    df.to_csv(f"data/{filename}", index=False)
    print(f"Saved data to data/{filename}")

def load_data(filename):
    """Load data from CSV"""
    return pd.read_csv(f"data/{filename}")