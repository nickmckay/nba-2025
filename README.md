# NBA Betting Pool 2025-26

A simple website to track an NBA betting pool where 6 players have 5 teams each, earning $0.25 per win and losing $0.25 per loss.

## Players and Teams

- **Dad**: Magic, Pistons, Pacers, Suns, Jazz
- **Tyler**: Heat, Thunder, Bucks, Raptors, Nets
- **Ethan**: 76ers, Mavericks, Grizzlies, Hawks, Celtics
- **Landon**: Trail Blazers, Clippers, Wizards, Knicks, Lakers
- **Mom**: Rockets, Nuggets, Spurs, Kings, Bulls
- **Micah**: Timberwolves, Warriors, Cavaliers, Hornets, Pelicans

## Features

- Live standings and leaderboard
- Automatic nightly updates via GitHub Actions
- Responsive design for mobile and desktop
- Real-time NBA data from the NBA API

## Setup

### GitHub Pages

1. Go to repository Settings > Pages
2. Under "Source", select "Deploy from a branch"
3. Select the `main` branch and `/ (root)` folder
4. Click Save

The site will be available at: `https://<username>.github.io/nba-2025/`

### GitHub Actions Permissions

1. Go to repository Settings > Actions > General
2. Under "Workflow permissions", select "Read and write permissions"
3. Click Save

This allows the GitHub Action to commit updated standings automatically.

## How It Works

1. **Data Source**: Uses the `nba_api` Python package to fetch official NBA standings
2. **Update Schedule**: GitHub Actions runs daily at 6 AM ET to update standings
3. **Calculations**: Script compares previous day's records with current records to calculate changes
4. **Automatic Deployment**: GitHub Pages automatically rebuilds when data is updated

## Manual Update

You can manually trigger an update:
1. Go to Actions tab
2. Select "Update NBA Standings" workflow
3. Click "Run workflow"

## Local Development

To test the update script locally:

```bash
cd scripts
pip install -r requirements.txt
python update_standings.py
```

To view the site locally, open `index.html` in a browser or use a local server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`

## Technologies

- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Backend**: Python with nba_api
- **Automation**: GitHub Actions
- **Hosting**: GitHub Pages
