// Load live bot stats
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
            const item = document.createElement("option");
            item.value = g.id;
            item.textContent = g.name;
            select.appendChild(item);
        });

        // Auto-load first guild info
        if (guilds.length > 0) {
            loadGuildInfo(guilds[0].id);
        }

    } catch (err) {
        console.log("Guild load error:", err);
    }
}

// Load selected guild info
async function loadGuildInfo(id) {
    try {
        const res = await fetch(`/api/guild/${id}/info`);
        const g = await res.json();

        const box = document.getElementById("guild-info-box");
        box.innerHTML = `
            <h3 class="gold-animate">${g.name}</h3>
            <p><b>ID:</b> ${g.id}</p>
            <p><b>Members:</b> ${g.member_count}</p>
            <p><b>Owner:</b> ${g.owner}</p>
            <p><b>Roles:</b> ${g.roles.join(", ")}</p>
        `;

    } catch (err) {
        console.log("Guild info error:", err);
    }
}

// Send bot command
async function sendBotCommand(cmd) {
    try {
        const res = await fetch(`/api/control/${cmd}`);
        const data = await res.json();
        alert(data.status || data.error);
    } catch (err) {
        alert("Failed to send command.");
    }
}

// Dropdown listener
document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("guild-select");
    select.addEventListener("change", () => loadGuildInfo(select.value));
});

setInterval(loadStats, 2000);
loadStats();
loadGuilds();
