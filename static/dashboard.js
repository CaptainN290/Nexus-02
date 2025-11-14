// Load bot stats
async function loadStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();

        document.getElementById("dashboard-stats").innerHTML = `
            <h3 class="gold-animate">Live Bot Stats</h3>
            <p><b>Ping:</b> ${data.ping}</p>
            <p><b>Uptime:</b> ${data.uptime}</p>
            <p><b>Servers:</b> ${data.servers}</p>
            <p><b>Users:</b> ${data.users}</p>
            <p><b>CPU:</b> ${data.cpu}%</p>
            <p><b>RAM:</b> ${data.memory}%</p>
            <p><b>OS:</b> ${data.os}</p>
        `;
    } catch (err) {
        console.log("Stats error:", err);
    }
}

// Load guild list
async function loadGuilds() {
    try {
        const res = await fetch("/api/guilds");
        const guilds = await res.json();

        let select = document.getElementById("guild-select");
        select.innerHTML = "";

        guilds.forEach(g => {
            let opt = document.createElement("option");
            opt.value = g.id;
            opt.innerText = g.name;
            select.appendChild(opt);
        });
    } catch (err) {
        console.log("Guild load error:", err);
    }
}

// Send bot command
async function sendBotCommand(cmd) {
    await fetch(`/api/control/${cmd}`);
    alert(`Command sent: ${cmd}`);
}

setInterval(loadStats, 2000);
loadStats();
loadGuilds();
