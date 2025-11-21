// ----------------------- Load Stats --------------------------
async function loadStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();

        document.getElementById("dashboard-stats").innerHTML = `
            <h3 class="gold-animate">Bot Status</h3>
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


// ----------------------- Load Guilds --------------------------
async function loadGuilds() {
    const res = await fetch("/api/guilds");
    const guilds = await res.json();

    const select = document.getElementById("guild-select");
    select.innerHTML = "";

    guilds.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g.id;
        opt.textContent = g.name;
        select.appendChild(opt);
    });

    if (guilds.length > 0) loadGuildInfo(guilds[0].id);
}


// ----------------------- Guild Info --------------------------
async function loadGuildInfo(id) {
    const res = await fetch(`/api/guild/${id}/info`);
    const data = await res.json();

    document.getElementById("guild-info-box").innerHTML = `
        <h3 class="gold-animate">${data.name}</h3>
        <p><b>ID:</b> ${data.id}</p>
        <p><b>Members:</b> ${data.members}</p>
    `;

    loadMembers(id);
    loadRoles(id);
}


// ----------------------- Members + Kick/Ban --------------------------
async function loadMembers(id) {
    const box = document.getElementById("guild-members-box");
    const res = await fetch(`/api/guild/${id}/members`);
    const data = await res.json();

    box.innerHTML = `<h3 class="gold-animate">Members</h3>`;

    data.members.forEach(m => {
        const row = document.createElement("div");
        row.className = "member-row";
        row.innerHTML = `
            <span>${m.name}</span>
            <div>
                <button onclick="kickMember(${id}, ${m.id})">Kick</button>
                <button onclick="banMember(${id}, ${m.id})">Ban</button>
            </div>
        `;
        box.appendChild(row);
    });
}

async function kickMember(gid, mid) {
    await fetch(`/api/guild/${gid}/kick`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({member_id: mid})
    });
    alert("Member kicked.");
}

async function banMember(gid, mid) {
    await fetch(`/api/guild/${gid}/ban`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({member_id: mid})
    });
    alert("Member banned.");
}


// ----------------------- Roles --------------------------
async function loadRoles(id) {
    const roleBox = document.getElementById("guild-role-box");
    const res = await fetch(`/api/guild/${id}/roles`);
    const data = await res.json();

    let roleHTML = "";
    data.roles.forEach(r => {
        roleHTML += `<button class="role-btn" onclick="toggleRole(${id}, '${r.id}')">${r.name}</button>`;
    });

    document.getElementById("role-list").innerHTML = roleHTML;
}

async function toggleRole(gid, rid) {
    alert("Role applied (not stored permanently).");
}


// ----------------------- Controls --------------------------
async function sendBotCommand(cmd) {
    const res = await fetch(`/api/control/${cmd}`);
    const data = await res.json();
    alert(data.status || data.error);
}


document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("guild-select");
    select.addEventListener("change", () => loadGuildInfo(select.value));
});

setInterval(loadStats, 2000);
loadStats();
loadGuilds();

// call /api/me to know who is logged in and which guilds are manageable
async function loadViewer() {
    try {
        const res = await fetch("/api/me");
        const data = await res.json();
        if (!data || data.logged_in !== true) {
            // not logged in
            const sel = document.getElementById("guild-select");
            if (sel) sel.innerHTML = `<option>Please sign in via Discord (click 'Connect' on the site)</option>`;
            document.getElementById("guild-info-box").innerHTML = `<p class="gold-animate">Not signed in. Use <strong>n/connect</strong> in Discord to link.</p>`;
            return;
        }

        // show viewer info
        const viewerBox = document.getElementById("viewer-box");
        if (viewerBox) {
            viewerBox.innerHTML = `<p class="gold-animate">Signed in as <b>${data.username}</b></p>`;
        }

        // populate manageable guilds
        const sel = document.getElementById("guild-select");
        if (!sel) return;
        sel.innerHTML = "";
        if (!data.manageable_guilds || data.manageable_guilds.length === 0) {
            sel.innerHTML = `<option>No manageable servers found.</option>`;
            return;
        }
        data.manageable_guilds.forEach(g => {
            const item = document.createElement("option");
            item.value = g.id;
            item.textContent = g.name;
            sel.appendChild(item);
        });

        // optionally auto-load first guild info:
        sel.dispatchEvent(new Event('change'));
    } catch (err) {
        console.error("loadViewer error", err);
    }
}

// call at DOM ready, plus existing loadStats/loadGuilds
document.addEventListener("DOMContentLoaded", () => {
    if (typeof loadViewer === "function") {
        loadViewer();
    }
});
