# ===== Fake audioop for Python 3.13 =====
import sys
import types

sys.modules['audioop'] = types.ModuleType('audioop')
# ========================================

# main.py

import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from typing import Optional
from datetime import timedelta

# ------------------- Flask Setup for Uptime -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
# -------------------------------------------------------------

# ------------------- Discord Bot Setup -----------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="n/", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ------------------- HELP COMMAND -----------------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Nexus Bot - Command List",
        description="Complete list of available commands",
        color=discord.Color.blue()
    )

    embed.add_field(name="🛡️ Moderation", value=(
        "`n/kick @user <reason>`\n"
        "`n/ban @user <reason>`\n"
        "`n/unban <user_id> <reason>`\n"
        "`n/timeout @user <minutes> <reason>`\n"
        "`n/removetimeout @user`\n"
        "`n/warn @user <reason>`\n"
        "`n/mute @user <reason>`\n"
        "`n/unmute @user`\n"
        "`n/clear <amount>`"
    ), inline=False)

    embed.add_field(name="🔧 Channel", value=(
        "`n/slowmode <seconds>`\n"
        "`n/lock`\n"
        "`n/unlock`"
    ), inline=False)

    embed.add_field(name="👥 Roles", value=(
        "`n/addrole @user @role`\n"
        "`n/removerole @user @role`\n"
        "`n/rolecatalog`"
    ), inline=False)

    embed.add_field(name="📊 Info", value=(
        "`n/userinfo [@user]`\n"
        "`n/serverinfo`\n"
        "`n/serverbanner`\n"
        "`n/avatar [@user]`\n"
        "`n/ping`\n"
        "`n/time`"
    ), inline=False)

    embed.add_field(name="🎉 Fun & Utility", value=(
        "`n/say <message>`\n"
        '`n/poll "question" option1 option2...`\n'
        "`n/announce <message>`\n"
        "`n/hug @user`\n"
        "`n/hugall`\n"
        "`n/kiss @user`\n"
        "`n/flipcoin`\n"
        "`n/roll [sides]`\n"
        "`n/inspire`\n"
        "`n/meme`\n"
        "`n/joke`"
    ), inline=False)

    embed.add_field(name="ℹ️ Other", value="`n/help` - Show this message", inline=False)
    embed.set_footer(text="Made by @captainn29")

    await ctx.send(embed=embed)

# ------------------- Core Commands -----------------------
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency*1000)}ms")

@bot.command()
async def say(ctx, *, message: str):
    try: await ctx.message.delete()
    except: pass
    await ctx.send(message)

# ------------------- Moderation Commands -----------------------
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.kick_members:
        return await ctx.send("❌ You don't have permission to kick members!")
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason or 'No reason provided'}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send("❌ You don't have permission to ban members!")
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} has been banned. Reason: {reason or 'No reason provided'}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ You don't have permission to timeout members!")
    try:
        await member.timeout(timedelta(minutes=duration), reason=reason)
        await ctx.send(f"✅ {member.mention} timed out for {duration} minutes.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def removetimeout(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ You don't have permission to remove timeouts!")
    try:
        await member.timeout(None)
        await ctx.send(f"✅ Timeout removed from {member.mention}.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def unban(ctx, user_id: int, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send("❌ You don't have permission to unban members!")
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ {user.name} has been unbanned.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ You can't warn members!")
    embed = discord.Embed(title="⚠️ Warning", description=f"{member.mention} has been warned!", color=discord.Color.orange())
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Warned by", value=ctx.author.mention)
    await ctx.send(embed=embed)
    try: await member.send(f"⚠️ You have been warned in {ctx.guild.name}. Reason: {reason or 'No reason provided'}")
    except: await ctx.send("⚠️ Warning issued, but couldn't DM the user.")

# ------------------- Role Catalog (Sorted by Hierarchy) -----------------------
@bot.command()
async def rolecatalog(ctx):
    roles = sorted(ctx.guild.roles[1:], key=lambda r: r.position, reverse=True)  # skip @everyone, sort by hierarchy
    embed = discord.Embed(
        title=f"📘 Role Catalog - {ctx.guild.name}",
        description=f"Total Roles: **{len(roles)}** (highest → lowest)",
        color=discord.Color.purple()
    )
    for role in roles:
        embed.add_field(
            name=role.name,
            value=f"🆔 `{role.id}` | 👥 {len(role.members)} members | 🗓️ Created: {role.created_at.strftime('%Y-%m-%d')}",
            inline=False
        )
    await ctx.send(embed=embed)

# ------------------- Utility & Fun -----------------------
@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"🤗 {ctx.author.mention} hugged {member.mention}!")

@bot.command()
async def hugall(ctx):
    await ctx.send(f"🤗 {ctx.author.mention} sends hugs to everyone!")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"💋 {ctx.author.mention} kissed {member.mention}!")

@bot.command()
async def flipcoin(ctx):
    import random
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"🪙 The coin landed on **{result}**!")

@bot.command()
async def roll(ctx, sides: int = 6):
    import random
    if sides < 2: return await ctx.send("❌ Minimum sides is 2")
    result = random.randint(1, sides)
    await ctx.send(f"🎲 You rolled a {result} on a {sides}-sided die!")

@bot.command()
async def inspire(ctx):
    import requests
    try:
        res = requests.get("https://api.quotable.io/random").json()
        await ctx.send(f"💡 {res['content']} —{res['author']}")
    except:
        await ctx.send("❌ Couldn't fetch quote!")

@bot.command()
async def meme(ctx):
    import requests
    try:
        res = requests.get("https://meme-api.com/gimme").json()
        await ctx.send(res["url"])
    except:
        await ctx.send("❌ Couldn't fetch meme!")

@bot.command()
async def joke(ctx):
    import requests
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any").json()
        if res["type"] == "single":
            await ctx.send(f"😂 {res['joke']}")
        else:
            await ctx.send(f"😂 {res['setup']} ... {res['delivery']}")
    except:
        await ctx.send("❌ Couldn't fetch joke!")

@bot.command()
async def time(ctx):
    from datetime import datetime
    await ctx.send(f"⏰ Current UTC time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
async def serverbanner(ctx):
    if ctx.guild.banner:
        await ctx.send(ctx.guild.banner.url)
    else:
        await ctx.send("❌ This server has no banner.")

# ------------------- Run Bot -------------------------------
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("❌ Please set your DISCORD_TOKEN environment variable!")
else:
    bot.run(token)
