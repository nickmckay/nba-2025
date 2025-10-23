// Team ID mapping for ESPN logo URLs
const TEAM_LOGOS = {
    'Magic': 'https://a.espncdn.com/i/teamlogos/nba/500/orl.png',
    'Pistons': 'https://a.espncdn.com/i/teamlogos/nba/500/det.png',
    'Pacers': 'https://a.espncdn.com/i/teamlogos/nba/500/ind.png',
    'Suns': 'https://a.espncdn.com/i/teamlogos/nba/500/phx.png',
    'Jazz': 'https://a.espncdn.com/i/teamlogos/nba/500/utah.png',
    'Heat': 'https://a.espncdn.com/i/teamlogos/nba/500/mia.png',
    'Thunder': 'https://a.espncdn.com/i/teamlogos/nba/500/okc.png',
    'Bucks': 'https://a.espncdn.com/i/teamlogos/nba/500/mil.png',
    'Raptors': 'https://a.espncdn.com/i/teamlogos/nba/500/tor.png',
    'Nets': 'https://a.espncdn.com/i/teamlogos/nba/500/bkn.png',
    '76ers': 'https://a.espncdn.com/i/teamlogos/nba/500/phi.png',
    'Mavericks': 'https://a.espncdn.com/i/teamlogos/nba/500/dal.png',
    'Grizzlies': 'https://a.espncdn.com/i/teamlogos/nba/500/mem.png',
    'Hawks': 'https://a.espncdn.com/i/teamlogos/nba/500/atl.png',
    'Celtics': 'https://a.espncdn.com/i/teamlogos/nba/500/bos.png',
    'Trail Blazers': 'https://a.espncdn.com/i/teamlogos/nba/500/por.png',
    'Clippers': 'https://a.espncdn.com/i/teamlogos/nba/500/lac.png',
    'Wizards': 'https://a.espncdn.com/i/teamlogos/nba/500/wsh.png',
    'Knicks': 'https://a.espncdn.com/i/teamlogos/nba/500/ny.png',
    'Lakers': 'https://a.espncdn.com/i/teamlogos/nba/500/lal.png',
    'Rockets': 'https://a.espncdn.com/i/teamlogos/nba/500/hou.png',
    'Nuggets': 'https://a.espncdn.com/i/teamlogos/nba/500/den.png',
    'Spurs': 'https://a.espncdn.com/i/teamlogos/nba/500/sa.png',
    'Kings': 'https://a.espncdn.com/i/teamlogos/nba/500/sac.png',
    'Bulls': 'https://a.espncdn.com/i/teamlogos/nba/500/chi.png',
    'Timberwolves': 'https://a.espncdn.com/i/teamlogos/nba/500/min.png',
    'Warriors': 'https://a.espncdn.com/i/teamlogos/nba/500/gs.png',
    'Cavaliers': 'https://a.espncdn.com/i/teamlogos/nba/500/cle.png',
    'Hornets': 'https://a.espncdn.com/i/teamlogos/nba/500/cha.png',
    'Pelicans': 'https://a.espncdn.com/i/teamlogos/nba/500/no.png'
};

// Load and display NBA betting pool data
async function loadStandings() {
    try {
        const response = await fetch('data/standings.json');
        const data = await response.json();

        displayLastUpdated(data.last_updated);
        displayLeaderboard(data.players);
        displayPlayerDetails(data.players, data.team_records);
    } catch (error) {
        console.error('Error loading standings:', error);
        document.getElementById('leaderboardTable').innerHTML =
            '<p class="error">Error loading data. Please try again later.</p>';
    }
}

function displayLastUpdated(date) {
    const lastUpdatedElement = document.getElementById('lastUpdated');
    const formattedDate = new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    lastUpdatedElement.textContent = `Last updated: ${formattedDate}`;
}

function displayLeaderboard(players) {
    // Convert players object to array and sort by earnings
    const playerArray = Object.entries(players).map(([name, data]) => ({
        name,
        ...data
    }));

    playerArray.sort((a, b) => b.earnings - a.earnings);

    // Create table HTML
    let html = `
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>Record</th>
                    <th>Earnings</th>
                </tr>
            </thead>
            <tbody>
    `;

    playerArray.forEach((player, index) => {
        const earningsClass = player.earnings > 0 ? 'positive' :
                             player.earnings < 0 ? 'negative' : 'neutral';
        const earningsFormatted = player.earnings >= 0 ?
                                 `+$${player.earnings.toFixed(2)}` :
                                 `-$${Math.abs(player.earnings).toFixed(2)}`;

        html += `
            <tr>
                <td class="rank">${index + 1}</td>
                <td class="player-name">${player.name}</td>
                <td class="record">${player.wins}-${player.losses}</td>
                <td class="earnings ${earningsClass}">${earningsFormatted}</td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
    `;

    document.getElementById('leaderboardTable').innerHTML = html;
}

function displayPlayerDetails(players, teamRecords) {
    const playerGrid = document.getElementById('playerGrid');

    // Convert to array and sort by earnings for consistency
    const playerArray = Object.entries(players).map(([name, data]) => ({
        name,
        ...data
    }));

    playerArray.sort((a, b) => b.earnings - a.earnings);

    let html = '';

    playerArray.forEach(player => {
        const earningsClass = player.earnings > 0 ? 'positive' :
                             player.earnings < 0 ? 'negative' : 'neutral';
        const earningsFormatted = player.earnings >= 0 ?
                                 `+$${player.earnings.toFixed(2)}` :
                                 `-$${Math.abs(player.earnings).toFixed(2)}`;

        html += `
            <div class="player-card">
                <div class="player-card-header">
                    <div class="player-card-name">${player.name}</div>
                    <div class="player-card-earnings ${earningsClass}">${earningsFormatted}</div>
                    <div class="player-card-record">${player.wins}-${player.losses}</div>
                </div>
                <ul class="team-list">
        `;

        player.teams.forEach(team => {
            const record = teamRecords[team];
            const logoUrl = TEAM_LOGOS[team];
            html += `
                <li class="team-item">
                    <div class="team-info">
                        <img src="${logoUrl}" alt="${team}" class="team-logo" />
                        <span class="team-name">${team}</span>
                    </div>
                    <span class="team-record">${record.wins}-${record.losses}</span>
                </li>
            `;
        });

        html += `
                </ul>
            </div>
        `;
    });

    playerGrid.innerHTML = html;
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadStandings);
