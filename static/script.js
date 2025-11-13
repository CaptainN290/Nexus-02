async function loadStatus() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();

        if (document.getElementById("status-box")) {
            document.getElementById("status-box").innerHTML = `
                <h3 class="glow-gold">Bot Status</h3>
                <p><b>Ping:</b> ${data.ping}</p>
                <p><b>Uptime:</b> ${data.uptime}</p>
                <p><b>Servers:</b> ${data.servers}</p>
                <p><b>Users:</b> ${data.users}</p>
                <p><b>CPU:</b> ${data.cpu}%</p>
                <p><b>Memory:</b> ${data.memory}%</p>
            `;
        }

        if (document.getElementById("dashboard-stats")) {
            document.getElementById("dashboard-stats").innerHTML = `
                <h3 class="glow-gold">Live Statistics</h3>
                <p><b>Ping:</b> ${data.ping}</p>
                <p><b>Uptime:</b> ${data.uptime}</p>
                <p><b>Servers:</b> ${data.servers}</p>
                <p><b>Users:</b> ${data.users}</p>
                <p><b>CPU Usage:</b> ${data.cpu}%</p>
                <p><b>Memory Usage:</b> ${data.memory}%</p>
                <p><b>OS:</b> ${data.os}</p>
            `;
        }
    } catch (err) {
        console.log("Could not load stats:", err);
    }
}

setInterval(loadStatus, 2000);
loadStatus();
