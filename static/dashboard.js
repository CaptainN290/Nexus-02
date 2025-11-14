// ========== Live Bot Stats ==========
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

// ========== Guild list ==========
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

        if (guilds.length > 0) {
            loadGuildInfo(guilds[0].id);
            loadRoles(guilds[0].id);
            loadLogs(guilds[0].id);
            loadMessages(guilds[0].id);
            loadMembers(guilds[0].id);
        }

    } catch (err) {
        console.log("Guild load error:", err);
    }
}

// ========== Guild info (server details) ==========
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
            <p><b>Roles:</b> ${g.roles.length}</p>
        `;
    } catch (err) {
        console.log("Guild info error:", err);
    }
}

// ========== Audit logs ==========
async function loadLogs(id) {
    try {
        const res = await fetch(`/api/guild/${id}/logs`);
        const logs = await res.json();
        const container = document.getElementById("logs-box");
        if (!container) return;
        container.innerHTML = `<h3 class="gold-animate">Recent Audit Logs</h3>`;
        if (logs.error) {
            container.innerHTML += `<p>${logs.error}</p>`;
            return;
        }
        logs.slice(0,30).forEach(l => {
            const el = document.createElement("div");
            el.className = "log-line";
            el.innerHTML = `<b>${l.action}</b> • ${l.user} • ${l.target} <span class="muted">(${new Date(l.created_at).toLocaleString()})</span>`;
            container.appendChild(el);
        });
    } catch (err) {
        console.log("Logs error:", err);
    }
}

// ========== Recent messages ==========
async function loadMessages(id) {
    try {
        const res = await fetch(`/api/guild/${id}/messages`);
        const msgs = await res.json();
        const container = document.getElementById("messages-box");
        if (!container) return;
        container.innerHTML = `<h3 class="gold-animate">Recent Messages (preview)</h3>`;
        if (msgs.error) {
            container.innerHTML += `<p>${msgs.error}</p>`;
            return;
        }
        msgs.slice(0,40).forEach(m => {
            const el = document.createElement("div");
            el.className = "msg-line";
            el.innerHTML = `<b>${m.author}</b>: ${escapeHtml(m.content)} <span class="muted">(${new Date(m.created_at).toLocaleString()})</span>`;
            container.appendChild(el);
        });
    } catch (err) {
        console.log("Messages error:", err);
    }
}

// ========== Members list ==========
async function loadMembers(id) {
    try {
        const res = await fetch(`/api/guild/${id}/members`);
        const members = await res.json();
        const container = document.getElementById("members-box");
        if (!container) return;
        container.innerHTML = `<h3 class="gold-animate">Members (up to 500)</h3>`;
        if (members.error) {
            container.innerHTML += `<p>${members.error}</p>`;
            return;
        }
        // small search box
        let listHtml = `<input id="member-search" placeholder="Search members..." oninput="filterMembers()" />`;
        listHtml += `<div id="member-list">`;
        members.forEach(m => {
            listHtml += `<div class="member-row" data-name="${m.name.toLowerCase()}">
                <img class="avatar-xs" src="${m.avatar||'/static/default-avatar.png'}" />
                <div class="member-meta"><b>${m.display_name}</b><div class="muted">${m.roles.join(", ")}</div></div>
            </div>`;
        });
        listHtml += `</div>`;
        container.innerHTML += listHtml;
    } catch (err) {
        console.log("Members error:", err);
    }
}

function filterMembers() {
    const q = document.getElementById("member-search").value.toLowerCase();
    document.querySelectorAll("#member-list .member-row").forEach(row => {
        const name = row.getAttribute("data-name");
        row.style.display = name.includes(q) ? "" : "none";
    });
}

// ========== Roles ==========
async function loadRoles(id) {
    try {
        const res = await fetch(`/api/guild/${id}/roles`);
        const roles = await res.json();
        const container = document.getElementById("roles-box");
        if (!container) return;
        container.innerHTML = `<h3 class="gold-animate">Roles</h3>`;
        if (roles.error) {
            container.innerHTML += `<p>${roles.error}</p>`;
            return;
        }
        roles.forEach(r => {
            const el = document.createElement("div");
            el.className = "role-row";
            el.innerHTML = `<b>${r.name}</b> <span class="muted">(${r.id})</span>`;
            container.appendChild(el);
        });
    } catch (err) {
        console.log("Roles error:", err);
    }
}

// ========== Assign/Remove role (UI helper) ==========
async function assignRole(guildId, memberId, roleId, action) {
    try {
        const res = await fetch(`/api/guild/${guildId}/role/assign`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({member_id: memberId, role_id: roleId, action: action})
        });
        const d = await res.json();
        alert(d.status || d.error || JSON.stringify(d));
    } catch (err) {
        alert("Role action failed");
    }
}

// small helper
function escapeHtml(s){
    if(!s) return "";
    return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// ========== wire up selectors ==========
document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById("guild-select");
    if (select) {
        select.addEventListener("change", () => {
            const id = select.value;
            loadGuildInfo(id);
            loadRoles(id);
            loadLogs(id);
            loadMessages(id);
            loadMembers(id);
        });
    }
});

// periodic refresh
setInterval(() => {
    const s = document.getElementById("guild-select");
    if (s && s.value) {
        const id = s.value;
        loadLogs(id);
        loadMessages(id);
    }
    loadStats();
}, 4000);

loadStats();
loadGuilds();
