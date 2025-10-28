# ===== Fake audioop for Python 3.13 =====
import sys, types
sys.modules['audioop'] = types.ModuleType('audioop')
# ========================================

# =================== Imports ===================
import os
import threading
import random
import requests
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from flask import Flask
import discord
from discord.ext import commands

# =================== Flask Setup (for uptime) ===================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Nexus Bot is running and healthy!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# =================== Discord Bot Setup ===================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="n/", intents=intents, help_command=None)

# =================== Events ===================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")
    for guild in bot.guilds:
        print(f"🔹 Connected to {guild.name} ({guild.id})")

@bot.event
async def on_command_error(ctx, error):
    import traceback
    traceback.print_exc()
    await ctx.send(f"❌ [Error: {error}]")

# =================== HELP COMMAND ===================
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🤖 Nexus Bot - Command List",
        description="Full list of available commands",
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
        "`n/timeGMT | n/timeEST | n/timePST | n/timeUTC`"
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

# =================== CORE COMMANDS ===================
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 [Pong!] Latency: {round(bot.latency * 1000)}ms")

@bot.command()
async def say(ctx, *, message: str):
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(message)

# =================== MODERATION COMMANDS ===================
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.kick_members:
        return await ctx.send("❌ [You don't have permission to kick members!]")
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ [{member.mention} has been kicked] Reason: {reason or 'No reason provided'}")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send("❌ [You don't have permission to ban members!]")
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ [{member.mention} has been banned] Reason: {reason or 'No reason provided'}")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def unban(ctx, user_id: int, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send("❌ [You don't have permission to unban members!]")
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ [{user.name} has been unbanned]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ [You don't have permission to timeout members!]")
    try:
        await member.timeout(timedelta(minutes=duration), reason=reason)
        await ctx.send(f"✅ [{member.mention} timed out for {duration} minutes]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def removetimeout(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ [You don't have permission to remove timeouts!]")
    try:
        await member.timeout(None)
        await ctx.send(f"✅ [Timeout removed from {member.mention}]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ [You can't warn members!]")
    embed = discord.Embed(title="⚠️ [Warning Issued]", description=f"{member.mention} has been warned.", color=discord.Color.orange())
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Warned by", value=ctx.author.mention)
    await ctx.send(embed=embed)
    try:
        await member.send(f"⚠️ You have been warned in {ctx.guild.name}. Reason: {reason or 'No reason provided'}")
    except:
        await ctx.send("⚠️ [Warning issued, but couldn't DM the user]")

@bot.command()
async def clear(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send("❌ [You don't have permission to delete messages!]")
    if amount < 1 or amount > 100:
        return await ctx.send("❌ [Amount must be between 1–100]")
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"✅ [Deleted {len(deleted) - 1} messages!]")
    await msg.delete(delay=3)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ [No permission!]")
    try:
        await member.timeout(timedelta(days=28), reason=reason)
        await ctx.send(f"🔇 [{member.mention} muted]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ [No permission!]")
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 [{member.mention} unmuted!]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def slowmode(ctx, seconds: int):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("❌ [No permission!]")
    if seconds < 0 or seconds > 21600:
        return await ctx.send("❌ [Slowmode must be 0–21600 seconds]")
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"✅ [Slowmode set to {seconds} seconds]" if seconds else "✅ [Slowmode disabled]")

@bot.command()
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("❌ [No permission!]")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 [Channel Locked]")

@bot.command()
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("❌ [No permission!]")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send("🔓 [Channel Unlocked]")

# =================== INFO COMMANDS ===================
@bot.command()
async def userinfo(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Nickname", value=member.nick or "None")
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown")
    embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles[1:]]) or "None")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.blue())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown")
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.blue())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverbanner(ctx):
    if ctx.guild.banner:
        await ctx.send(ctx.guild.banner.url)
    else:
        await ctx.send("❌ [This server has no banner]")

# ----- Time Commands -----
@bot.command()
async def timeGMT(ctx):
    tz = ZoneInfo("Etc/GMT")
    now = datetime.now(tz)
    await ctx.send(f"⏰ [Current Time (GMT)]: {now.strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
async def timeEST(ctx):
    tz = ZoneInfo("America/New_York")
    now = datetime.now(tz)
    await ctx.send(f"⏰ [Current Time (EST)]: {now.strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
async def timePST(ctx):
    tz = ZoneInfo("America/Los_Angeles")
    now = datetime.now(tz)
    await ctx.send(f"⏰ [Current Time (PST)]: {now.strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
async def timeUTC(ctx):
    now = datetime.utcnow()
    await ctx.send(f"⏰ [Current Time (UTC)]: {now.strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
async def rolecatalog(ctx):
    roles = sorted(ctx.guild.roles[1:], key=lambda r: r.position, reverse=True)
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

# =================== ROLE MANAGEMENT ===================
@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if not ctx.author.guild_permissions.manage_roles:
        return await ctx.send("❌ [No permission!]")
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ [Added {role.mention} to {member.mention}]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if not ctx.author.guild_permissions.manage_roles:
        return await ctx.send("❌ [No permission!]")
    try:
        await member.remove_roles(role)
        await ctx.send(f"✅ [Removed {role.mention} from {member.mention}]")
    except Exception as e:
        await ctx.send(f"❌ [Error: {e}]")

# =================== FUN & UTILITY ===================
@bot.command()
async def poll(ctx, question: str, *options):
    if len(options) < 2:
        return await ctx.send("❌ [Minimum 2 options required]")
    if len(options) > 10:
        return await ctx.send("❌ [Maximum 10 options allowed]")
    reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    description = "\n".join([f"{reactions[i]} {opt}" for i, opt in enumerate(options)])
    embed = discord.Embed(title=f"📊 {question}", description=description, color=discord.Color.green())
    embed.set_footer(text=f"Poll by {ctx.author}")
    poll_message = await ctx.send(embed=embed)
    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])

@bot.command()
async def announce(ctx, *, message: str):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send("❌ [No permission!]")
    embed = discord.Embed(title="📢 [Announcement]", description=message, color=discord.Color.gold())
    embed.set_footer(text=f"Announced by {ctx.author}")
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"🤗 [{ctx.author.mention} hugged {member.mention}]")

@bot.command()
async def hugall(ctx):
    await ctx.send(f"🤗 [{ctx.author.mention} sends hugs to everyone!]")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"💋 [{ctx.author.mention} kissed {member.mention}]")

@bot.command()
async def flipcoin(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"🪙 [The coin landed on {result}]")

@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 2:
        return await ctx.send("❌ [Minimum sides is 2]")
    result = random.randint(1, sides)
    await ctx.send(f"🎲 [You rolled a {result} on a {sides}-sided die]")

@bot.command()
async def inspire(ctx):
    try:
        res = requests.get("https://api.quotable.io/random").json()
        await ctx.send(f"💡 [{res['content']} —{res['author']}]")
    except:
        await ctx.send("❌ [Couldn't fetch quote]")

@bot.command()
async def meme(ctx):
    try:
        res = requests.get("https://meme-api.com/gimme").json()
        await ctx.send(res["url"])
    except:
        await ctx.send("❌ [Couldn't fetch meme]")

@bot.command()
async def joke(ctx):
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any").json()
        if res["type"] == "single":
            await ctx.send(f"😂 [{res['joke']}]")
        else:
            await ctx.send(f"😂 [{res['setup']} ... {res['delivery']}]")
    except:
        await ctx.send("❌ [Couldn't fetch joke]")

# =================== RUN BOT ===================
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("❌ Please set your DISCORD_TOKEN environment variable!")
else:
    bot.run(token)
