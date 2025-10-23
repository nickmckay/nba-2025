#!/usr/bin/env python3
"""
NBA Betting Pool Standings Updater
Fetches NBA game results and updates player standings.
"""

import json
import os
from datetime import datetime, timedelta
from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams

# Team name mappings (NBA API names to our display names)
TEAM_NAME_MAP = {
    'Orlando Magic': 'Magic',
    'Detroit Pistons': 'Pistons',
    'Indiana Pacers': 'Pacers',
    'Phoenix Suns': 'Suns',
    'Utah Jazz': 'Jazz',
    'Miami Heat': 'Heat',
    'Oklahoma City Thunder': 'Thunder',
    'Milwaukee Bucks': 'Bucks',
    'Toronto Raptors': 'Raptors',
    'Brooklyn Nets': 'Nets',
    'Philadelphia 76ers': '76ers',
    'Dallas Mavericks': 'Mavericks',
    'Memphis Grizzlies': 'Grizzlies',
    'Atlanta Hawks': 'Hawks',
    'Boston Celtics': 'Celtics',
    'Portland Trail Blazers': 'Trail Blazers',
    'LA Clippers': 'Clippers',
    'Washington Wizards': 'Wizards',
    'New York Knicks': 'Knicks',
    'Los Angeles Lakers': 'Lakers',
    'Houston Rockets': 'Rockets',
    'Denver Nuggets': 'Nuggets',
    'San Antonio Spurs': 'Spurs',
    'Sacramento Kings': 'Kings',
    'Chicago Bulls': 'Bulls',
    'Minnesota Timberwolves': 'Timberwolves',
    'Golden State Warriors': 'Warriors',
    'Cleveland Cavaliers': 'Cavaliers',
    'Charlotte Hornets': 'Hornets',
    'New Orleans Pelicans': 'Pelicans'
}

# Reverse mapping for lookup
REVERSE_TEAM_MAP = {v: k for k, v in TEAM_NAME_MAP.items()}

def get_nba_team_id(team_name):
    """Get NBA team ID from team name."""
    all_teams = teams.get_teams()
    full_name = REVERSE_TEAM_MAP.get(team_name)
    if not full_name:
        return None

    for team in all_teams:
        if team['full_name'] == full_name:
            return team['id']
    return None

def get_games_for_date(date):
    """Fetch games for a specific date."""
    try:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=date.strftime('%Y-%m-%d'))
        games_df = scoreboard.game_header.get_data_frame()
        return games_df
    except Exception as e:
        print(f"Error fetching games for {date}: {e}")
        return None

def parse_games(games_df):
    """Parse games dataframe and return list of results."""
    if games_df is None or games_df.empty:
        return []

    results = []
    all_teams = teams.get_teams()
    team_id_to_name = {team['id']: team['full_name'] for team in all_teams}

    for _, game in games_df.iterrows():
        home_team_id = game['HOME_TEAM_ID']
        visitor_team_id = game['VISITOR_TEAM_ID']

        home_team_name = team_id_to_name.get(home_team_id, 'Unknown')
        visitor_team_name = team_id_to_name.get(visitor_team_id, 'Unknown')

        # Map to our display names
        home_team = TEAM_NAME_MAP.get(home_team_name)
        visitor_team = TEAM_NAME_MAP.get(visitor_team_name)

        if not home_team or not visitor_team:
            continue

        # Determine winner (game must be final)
        game_status = game.get('GAME_STATUS_TEXT', '')
        if 'Final' not in game_status:
            continue

        # Parse scores from the line score
        # The game_header doesn't have scores, we need to check if game is finished
        # For simplicity, we'll use the standings endpoint instead
        continue

    return results

def get_team_standings():
    """Get current NBA team standings."""
    from nba_api.stats.endpoints import leaguestandings

    try:
        standings = leaguestandings.LeagueStandings()
        standings_df = standings.get_data_frames()[0]

        team_records = {}
        all_teams = teams.get_teams()
        team_id_to_name = {team['id']: team['full_name'] for team in all_teams}

        for _, row in standings_df.iterrows():
            team_id = row['TeamID']
            full_name = team_id_to_name.get(team_id)
            display_name = TEAM_NAME_MAP.get(full_name)

            if display_name:
                team_records[display_name] = {
                    'wins': int(row['WINS']),
                    'losses': int(row['LOSSES'])
                }

        return team_records
    except Exception as e:
        print(f"Error fetching standings: {e}")
        return None

def update_standings_file():
    """Update the standings JSON file."""
    # Get current standings from NBA API
    new_team_records = get_team_standings()

    if not new_team_records:
        print("Failed to fetch team standings")
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

    print(f"Updated standings successfully")
    print(f"Teams with changes: {len(changes)}")
    for team, change in changes.items():
        print(f"  {team}: +{change['wins']}W, +{change['losses']}L")

    return True

if __name__ == '__main__':
    success = update_standings_file()
    exit(0 if success else 1)
