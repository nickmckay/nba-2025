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
            html += `
                <li class="team-item">
                    <span class="team-name">${team}</span>
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
