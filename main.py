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
from datetime import timedelta, datetime

# ------------------- Flask Setup for Uptime -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

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
        "n/kick @user <reason>\n"
        "n/ban @user <reason>\n"
        "n/unban <user_id> <reason>\n"
        "n/timeout @user <minutes> <reason>\n"
        "n/removetimeout @user\n"
        "n/warn @user <reason>\n"
        "n/mute @user <reason>\n"
        "n/unmute @user\n"
        "n/clear <amount>"
    ), inline=False)
    embed.add_field(name="🔧 Channel", value=(
        "n/slowmode <seconds>\n"
        "n/lock\n"
        "n/unlock"
    ), inline=False)
    embed.add_field(name="👥 Roles", value=(
        "n/addrole @user @role\n"
        "n/removerole @user @role\n"
        "n/rolecatalog"
    ), inline=False)
    embed.add_field(name="📊 Info", value=(
        "n/userinfo [@user]\n"
        "n/serverinfo\n"
        "n/serverbanner\n"
        "n/avatar [@user]\n"
        "n/ping\n"
        "n/time"
    ), inline=False)
    embed.add_field(name="🎉 Fun & Utility", value=(
        "n/say <message>\n"
        'n/poll "question" option1 option2...\n'
        "n/announce <message>\n"
        "n/hug @user\n"
        "n/hugall\n"
        "n/kiss @user\n"
        "n/flipcoin\n"
        "n/roll [sides]"
    ), inline=False)
    embed.add_field(name="ℹ️ Other", value="n/help - Show this message", inline=False)
    embed.set_footer(text="Made by @captainn29")
    await ctx.send(embed=embed)

# ------------------- Core Commands -----------------------
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency*1000)}ms")

@bot.command()
async def say(ctx, *, message: str):
    try:
        await ctx.message.delete()
    except:
        pass
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
    try:
        await member.send(f"⚠️ You have been warned in {ctx.guild.name}. Reason: {reason or 'No reason provided'}")
    except:
        await ctx.send("⚠️ Warning issued, but couldn't DM the user.")

@bot.command()
async def clear(ctx, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send("❌ You don't have permission to delete messages!")
    if amount < 1 or amount > 100:
        return await ctx.send("❌ Amount must be between 1-100")
    deleted = await ctx.channel.purge(limit=amount+1)
    msg = await ctx.send(f"✅ Deleted {len(deleted)-1} messages!")
    await msg.delete(delay=3)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ No permission!")
    try:
        await member.timeout(timedelta(days=28), reason=reason)
        await ctx.send(f"🔇 {member.mention} muted.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send("❌ No permission!")
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} unmuted!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def slowmode(ctx, seconds: int):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("❌ No permission!")
    if seconds < 0 or seconds > 21600:
        return await ctx.send("❌ Slowmode must be 0-21600 seconds")
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"✅ Slowmode set to {seconds} seconds!" if seconds else "✅ Slowmode disabled!")

@bot.command()
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("❌ No permission!")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Channel locked!")

@bot.command()
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send("❌ No permission!")
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send("🔓 Channel unlocked!")

# ------------------- Info Commands -----------------------
@bot.command()
async def userinfo(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=member.color)
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
    embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member}'s Avatar")
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency*1000)}ms")

# ------------------- Fun Commands (kept, without joke/meme/inspire) -----------------------
@bot.command()
async def flipcoin(ctx):
    await ctx.send("🪙 " + random.choice(["Heads", "Tails"]))

@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 2:
        return await ctx.send("❌ Must be 2 or higher!")
    await ctx.send(f"🎲 You rolled a {random.randint(1, sides)}!")

# ------------------- Run Bot -----------------------
bot.run(os.environ["TOKEN"])
