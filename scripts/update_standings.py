#!/usr/bin/env python3
"""
NBA Betting Pool Standings Updater
Fetches NBA standings from ESPN and updates player standings.
"""

import json
import os
import time
from datetime import datetime
import requests

# Team name mappings (ESPN team abbreviations to our display names)
ESPN_TEAM_MAP = {
    'ORL': 'Magic',
    'DET': 'Pistons',
    'IND': 'Pacers',
    'PHX': 'Suns',
    'UTAH': 'Jazz',
    'MIA': 'Heat',
    'OKC': 'Thunder',
    'MIL': 'Bucks',
    'TOR': 'Raptors',
    'BKN': 'Nets',
    'PHI': '76ers',
    'DAL': 'Mavericks',
    'MEM': 'Grizzlies',
    'ATL': 'Hawks',
    'BOS': 'Celtics',
    'POR': 'Trail Blazers',
    'LAC': 'Clippers',
    'WSH': 'Wizards',
    'NY': 'Knicks',
    'LAL': 'Lakers',
    'HOU': 'Rockets',
    'DEN': 'Nuggets',
    'SA': 'Spurs',
    'SAC': 'Kings',
    'CHI': 'Bulls',
    'MIN': 'Timberwolves',
    'GS': 'Warriors',
    'CLE': 'Cavaliers',
    'CHA': 'Hornets',
    'NO': 'Pelicans'
}

def get_team_standings_espn(max_retries=3):
    """Get current NBA team standings from ESPN API."""
    # Use 2026 for the 2025-26 season
    url = "https://site.web.api.espn.com/apis/v2/sports/basketball/nba/standings?season=2026"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for attempt in range(max_retries):
        try:
            print(f"Fetching standings from ESPN (attempt {attempt + 1}/{max_retries})...")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            team_records = {}

            # ESPN API structure: children contains conferences (Eastern/Western)
            if 'children' in data and len(data['children']) > 0:
                for conference in data['children']:
                    if 'standings' in conference and 'entries' in conference['standings']:
                        standings = conference['standings']['entries']

                        for entry in standings:
                            team = entry['team']
                            stats = entry['stats']

                            # Get team abbreviation
                            abbrev = team['abbreviation']
                            display_name = ESPN_TEAM_MAP.get(abbrev)

                            if display_name:
                                # Find wins and losses in stats
                                wins = 0
                                losses = 0

                                for stat in stats:
                                    if stat['name'] == 'wins':
                                        wins = int(stat['value'])
                                    elif stat['name'] == 'losses':
                                        losses = int(stat['value'])

                                team_records[display_name] = {
                                    'wins': wins,
                                    'losses': losses
                                }

            if len(team_records) == 30:
                print(f"Successfully fetched standings for {len(team_records)} teams")
                return team_records
            else:
                print(f"Warning: Only found {len(team_records)} teams")
                if len(team_records) > 0:
                    return team_records

        except requests.exceptions.Timeout:
            print(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

    return None

def update_standings_file():
    """Update the standings JSON file."""
    # Get current standings from ESPN
    new_team_records = get_team_standings_espn()

    if not new_team_records:
        print("Failed to fetch team standings after all retries")
        return False

    # Load current data
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'standings.json')

    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Data file not found: {data_file}")
        return False

    old_team_records = data['team_records']

    # Calculate changes for each team
    changes = {}
    for team, new_record in new_team_records.items():
        if team in old_team_records:
            old_record = old_team_records[team]
            wins_diff = new_record['wins'] - old_record['wins']
            losses_diff = new_record['losses'] - old_record['losses']

            if wins_diff > 0 or losses_diff > 0:
                changes[team] = {
                    'wins': wins_diff,
                    'losses': losses_diff
                }

    # Update player earnings based on team changes
    for player_name, player_data in data['players'].items():
        player_teams = player_data['teams']

        for team in player_teams:
            if team in changes:
                # Add wins
                player_data['wins'] += changes[team]['wins']
                player_data['earnings'] += changes[team]['wins'] * 0.25

                # Add losses
                player_data['losses'] += changes[team]['losses']
                player_data['earnings'] -= changes[team]['losses'] * 0.25

        # Round earnings to 2 decimal places
        player_data['earnings'] = round(player_data['earnings'], 2)

    # Update team records
    data['team_records'] = new_team_records

    # Update last updated date
    data['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Write updated data
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Updated standings successfully")
    print(f"Teams with changes: {len(changes)}")
    if changes:
        for team, change in changes.items():
            print(f"  {team}: +{change['wins']}W, +{change['losses']}L")
    else:
        print("  No games played since last update")

    return True

if __name__ == '__main__':
    success = update_standings_file()
    exit(0 if success else 1)
