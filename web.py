from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder="static", template_folder="templates")

# Home
@app.route("/")
def home():
    return render_template("index.html")

# Commands docs
@app.route("/commands")
def commands():
    # Static command/categories data (edit here to update website)
    commands_data = [
        {
            "category": "⛊ Moderation",
            "items": [
                {"name": "n/kick @user <reason>", "desc": "Remove a member from the server. Requires 'Kick Members' permission."},
                {"name": "n/ban @user <reason>", "desc": "Permanently ban a user from the server. Requires 'Ban Members' permission."},
                {"name": "n/unban <user_id>", "desc": "Unban a previously banned user by their ID."},
                {"name": "n/timeout @user <minutes> <reason>", "desc": "Temporarily restrict a user from speaking or interacting."},
                {"name": "n/removetimeout @user", "desc": "Lift an active timeout and restore user permissions."},
                {"name": "n/mute @user <reason>", "desc": "Prevent a member from sending messages in text channels."},
                {"name": "n/unmute @user", "desc": "Remove a mute from a user."},
                {"name": "n/warn @user <reason>", "desc": "Issue a formal warning to a user; useful for staff logs."},
                {"name": "n/snipe [0-5] [#channel]", "desc": "Retrieve recently deleted messages (up to 5) for moderation review."},
                {"name": "n/clear <amount> [ex:] [images/@user]", "desc": "Bulk delete messages; optional filters: images or a specific user."},
                {"name": "n/setupapp #channel <title> - <question> | <question>", "desc": "Create and configure an application form that will send submissions to the selected channel for staff review."},
                {"name": "n/openapp [@user]", "desc": "Open or submit an application for the invoking user (or for a specified user)."}
            ]
        },
        {
            "category": "⚙︎ Channel",
            "items": [
                {"name": "n/slowmode <seconds>", "desc": "Enable slowmode in the channel, limiting how often users can post."},
                {"name": "n/lock", "desc": "Lock the current channel so non-staff cannot send messages."},
                {"name": "n/unlock", "desc": "Unlock the current channel and restore send permissions."}
            ]
        },
        {
            "category": "𐀪 Roles",
            "items": [
                {"name": "n/addrole @user @role", "desc": "Assign a specific role to a member."},
                {"name": "n/removerole @user @role", "desc": "Remove a role from a member."},
                {"name": "n/rolecatalog", "desc": "Show a list of server roles (limit: 20) for quick selection."}
            ]
        },
        {
            "category": "𝒊 Info",
            "items": [
                {"name": "n/userinfo @user", "desc": "Show detailed user information (join date, roles, ID, status)."},
                {"name": "n/serverinfo", "desc": "Display server statistics and settings overview."},
                {"name": "n/serverbanner", "desc": "Display the server banner image (if available)."},
                {"name": "n/avatar @user", "desc": "View a user's avatar in full size."},
                {"name": "n/ping", "desc": "Check the bot's latency."},
                {"name": "n/time", "desc": "Show the current UTC time."},
                {"name": "n/status", "desc": "Show the bot's operational status and web service connection."},
                {"name": "n/invite", "desc": "Get a link to invite the bot to another server."}
            ]
        },
        {
            "category": "☻ Fun & Games",
            "items": [
                {"name": "n/hug @user", "desc": "Send a virtual hug to another user."},
                {"name": "n/hugall", "desc": "Hug everyone in the server at once."},
                {"name": "n/kiss @user", "desc": "Kiss another user."},
                {"name": "n/flipcoin", "desc": "Flip a coin (heads or tails)."},
                {"name": "n/roll <sides> or n/roll 0d0", "desc": "Roll dice with a customizable number of sides."},
                {"name": "n/8ball <question>", "desc": "Ask for a simple yes/no/maybe answer from the 8-ball."},
                {"name": "n/meme", "desc": "Retrieve a random meme from the configured source."},
                {"name": "n/rps <rock/paper/scissors>", "desc": "Play rock-paper-scissors with the bot."},
                {"name": "n/tictactoe @opponent", "desc": "Start a Tic Tac Toe match with another user."},
                {"name": "n/tttmove <1-9>", "desc": "Make a move in an active Tic Tac Toe game."},
                {"name": "n/connect4 @opponent", "desc": "Start Connect 4 against another user."},
                {"name": "n/c4move <1-7>", "desc": "Drop a token into a column for Connect 4."},
                {"name": "n/rpg", "desc": "Begin an interactive text-based RPG session."},
                {"name": "n/spellduel @opponent", "desc": "Duel another user with spells and abilities."},
                {"name": "n/rapbattle @opponent", "desc": "Challenge a user to a rap battle."},
                {"name": "n/wordchain <word>", "desc": "Begin a word-chain game (next word must start with last letter)."},
                {"name": "n/endwordchain", "desc": "End the active word chain session."}
            ]
        },
        {
            "category": "⚡︎ Utility",
            "items": [
                {"name": "n/say <message>", "desc": "Make the bot repeat your message verbatim."},
                {"name": "n/poll \"question\" <option1> <option2> [0d 0h]", "desc": "Create a poll with options and an optional duration."},
                {"name": "n/announce <message>", "desc": "Post a styled announcement in the channel."},
                {"name": "n/ask <question>", "desc": "Ask the integrated AI assistant a question and receive a response."},
                {"name": "n/define <word>", "desc": "Lookup definitions, parts of speech, and examples for a word."}
            ]
        }
    ]

    return render_template("commands.html", commands_data=commands_data)

# Dashboard (static mock)
@app.route("/dashboard")
def dashboard():
    stats = {
        "guilds": 0,
        "users": 0,
        "latency": "N/A",
        "uptime": "N/A",
        "version": "Nexus Bot"
    }
    # You can update these stat values manually or later pull from your bot
    return render_template("dashboard.html", stats=stats)

if __name__ == "__main__":
    # Bind to 0.0.0.0 so Render can serve the site
    app.run(host="0.0.0.0", port=5000)
