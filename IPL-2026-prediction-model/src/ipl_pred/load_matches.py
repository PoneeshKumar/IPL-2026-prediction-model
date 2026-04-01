import json
import pathlib
import pandas as pd
from pathlib import Path
import os

# Make a function to load the mathes data from the JSON files and return it as a pandas DataFrame
def load_matches(path):
    """Load cricket matches data from a JSON file and return it as a pandas DataFrame."""
    raw_path = pathlib.Path(path)
    all_matches = []
    
    if not raw_path.exists():
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    # Read the JSON file and load the data
    for file_path in raw_path.glob('*.json'):
        if file_path.name == "README.txt":
            continue
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                
                #get the info section
                info = data.get('info', {})
                teams = info.get('teams', [None, None])

                #flatten into one dictionary
                match_data = {
                    'match_id': file_path.stem,
                    'season': info.get('season'),
                    'venue': info.get('venue'),
                    'city': info.get('city'),
                    'toss_winner': info.get('toss', {}).get('winner'),
                    'toss_decision': info.get('toss', {}).get('decision'),
                    'result': info.get('outcome', {}).get('result'),
                    'winner': info.get('outcome', {}).get('winner'),
                    'margin': info.get('outcome', {}).get('by', {}).get('runs') or info.get('outcome', {}).get('by', {}).get('wickets'),
                    'team1': teams[0],
                    'team2': teams[1],
            
                }
                all_matches.append(match_data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {file_path}")
    # Convert the list of match data into a pandas DataFrame
    matches_df = pd.DataFrame(all_matches)
    return matches_df


