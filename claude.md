# NBA Betting Pool 2025-26 - Development Notes

## Project Overview

A website that tracks an NBA betting pool where 6 players have 5 teams each, earning $0.25 per win and losing $0.25 per loss. The site is hosted on GitHub Pages and automatically updates nightly with the latest NBA standings.

## Technology Stack

- **Frontend**: Vanilla HTML, CSS, JavaScript (no frameworks)
- **Data Source**: ESPN public API
- **Automation**: GitHub Actions
- **Hosting**: GitHub Pages
- **Backend**: Python script with `requests` library

## Project Structure

```
/
├── index.html              # Main website page
├── styles.css              # Responsive styling with gradient background
├── script.js               # Frontend JS to load and display standings
├── data/
│   └── standings.json      # Current player standings and team records
├── scripts/
│   ├── update_standings.py # Python script to fetch NBA data
│   └── requirements.txt    # Python dependencies (just requests)
└── .github/
    └── workflows/
        └── update-standings.yml  # GitHub Actions workflow
```

## Players and Teams

- **Dad**: Magic, Pistons, Pacers, Suns, Jazz
- **Tyler**: Heat, Thunder, Bucks, Raptors, Nets
- **Ethan**: 76ers, Mavericks, Grizzlies, Hawks, Celtics
- **Landon**: Trail Blazers, Clippers, Wizards, Knicks, Lakers
- **Mom**: Rockets, Nuggets, Spurs, Kings, Bulls
- **Micah**: Timberwolves, Warriors, Cavaliers, Hornets, Pelicans

## Key Features

### Frontend
- Leaderboard sorted by earnings (highest to lowest)
- Color-coded earnings (green for positive, red for negative, gray for neutral)
- Player cards showing each player's teams with logos
- Team logos from ESPN CDN (32x32px)
- Responsive design for mobile and desktop
- Clean gradient background (purple theme)

### Backend (update_standings.py)
- Fetches standings from ESPN's public API
- Uses season parameter 2026 for 2025-26 NBA season
- Compares previous records with current records to calculate changes
- Updates player wins/losses/earnings incrementally
- Retry logic with exponential backoff (3 attempts, 30s timeout)
- Detailed logging of changes

### Automation
- Runs nightly at 6 AM ET (11 AM UTC)
- Runs on every push to main branch
- Can be triggered manually via workflow_dispatch
- Automatically commits updated standings.json
- GitHub Pages rebuilds automatically after commits

## Important Implementation Details

### ESPN API
- **Endpoint**: `https://site.web.api.espn.com/apis/v2/sports/basketball/nba/standings?season=2026`
- **Why ESPN?**: NBA.com's API (`stats.nba.com`) times out from GitHub Actions servers
- **Structure**: Returns two conferences (Eastern/Western), iterate through both
- **Team Mapping**: ESPN uses abbreviations (e.g., 'ORL', 'DET') mapped to display names

### Team Logos
- **Source**: ESPN CDN at `https://a.espncdn.com/i/teamlogos/nba/500/{abbrev}.png`
- **Abbreviations**: Match ESPN's team abbreviations (e.g., 'orl', 'gs', 'sa')
- **Display**: 32x32px with `object-fit: contain`

### GitHub Actions Permissions
- **Required**: `permissions: contents: write` in workflow
- **Why**: Allows the bot to commit and push updated standings
- **User**: github-actions[bot]

### Data Flow
1. GitHub Action triggers (schedule/push/manual)
2. Python script fetches ESPN standings
3. Script compares old vs new records
4. Updates player earnings based on team changes
5. Commits standings.json if changes detected
6. GitHub Pages auto-rebuilds
7. Website displays updated data

### Preventing Infinite Loops
- When workflow commits to main, it triggers another run
- Second run finds no changes (standings already updated)
- Exits cleanly without committing
- No infinite loop

## Season Configuration

- **Current Season**: 2025-26
- **ESPN Season Parameter**: 2026 (year the season ends)
- **Update in**: `index.html`, `data/standings.json`, `README.md`, `scripts/update_standings.py`

## Setup Instructions

### GitHub Pages Setup
1. Go to Settings > Pages
2. Source: "Deploy from a branch"
3. Branch: `main`
4. Folder: `/ (root)`

### GitHub Actions Permissions
1. Go to Settings > Actions > General
2. Workflow permissions: "Read and write permissions"
3. Save

### Manual Testing
```bash
# Test update script locally
python3 scripts/update_standings.py

# Serve site locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Troubleshooting

### Issue: GitHub Action timeout
- **Cause**: NBA.com blocks automated requests
- **Solution**: Use ESPN API instead

### Issue: 403 permission denied on push
- **Cause**: Missing write permissions
- **Solution**: Add `permissions: contents: write` to workflow

### Issue: Workflow runs in infinite loop
- **Cause**: Committing to main triggers another run
- **Solution**: Script only commits if changes detected (built-in)

## Future Enhancements

Potential improvements:
- Add game-by-game history
- Show recent performance trends
- Add player stats/comparisons
- Email notifications for daily updates
- Mobile app version

## Development History

1. Initial setup with static HTML/CSS/JS
2. Added ESPN API integration
3. Configured GitHub Actions for automation
4. Added team logos from ESPN CDN
5. Fixed timeout issues by switching from NBA API to ESPN
6. Added push trigger for easier testing
7. Configured proper GitHub Actions permissions
