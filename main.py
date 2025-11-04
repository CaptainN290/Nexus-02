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
from datetime import timedelta, datetime
from typing import Optional
import random
import asyncio
import re
import aiohttp

# ------------------- Flask Setup for Uptime -------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# ------------------- Discord Bot Setup -----------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="n/", intents=intents, help_command=None)
bot_start_time = datetime.utcnow()

# ------------------- Helper -----------------------
def no_perm_msg(action):
    return f"**❌ [You do not have permission to {action}]**"

# ------------------- Events -----------------------
@bot.event
async def on_ready():
    print(f"✅ [Logged in as {bot.user}]")

# ------------------- HELP COMMAND -----------------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="**➤ 𝐍𝐞𝐱𝐮𝐬 𝐁𝐨𝐭 - 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐋𝐢𝐬𝐭**",
        description="• List of all working commands",
        color=discord.Color.blue()
    )

    embed.add_field(name="**⛊ Moderation**", value=(
        "```"
        "n/kick @user <reason>\n"
        "n/ban @user <reason>\n"
        "n/unban <user_id>\n"
        "n/timeout @user <minutes> <reason>\n"
        "n/removetimeout @user\n"
        "n/mute @user <reason>\n"
        "n/unmute @user\n"
        "n/warn @user <reason>\n"
        "n/clear <amount> [images/users] ex: images"
        "```"
    ), inline=False)

    embed.add_field(name="**⚙︎ Channel**", value=(
        "```"
        "n/slowmode <seconds>\n"
        "n/lock\n"
        "n/unlock"
        "```"
    ), inline=False)

    embed.add_field(name="**𐀪 Roles**", value=(
        "```"
        "n/addrole @user @role\n"
        "n/removerole @user @role\n"
        "n/rolecatalog"
        "```"
    ), inline=False)

    embed.add_field(name="**𝒊 Info**", value=(
        "```"
        "n/userinfo [@user]\n"
        "n/serverinfo\n"
        "n/serverbanner\n"
        "n/avatar [@user]\n"
        "n/ping\n"
        "n/time\n"
        "n/status - Show bot and web service status"
        "```"
    ), inline=False)

    embed.add_field(name="**☻ Fun & Utility**", value=(
        "```"
        "n/say <message>\n"
        "n/poll \"question\" option1 option2 0d 0h\n"
        "n/announce <message>\n"
        "n/hug @user\n"
        "n/hugall\n"
        "n/kiss @user\n"
        "n/flipcoin\n"
        "n/roll [sides] or n/roll XdY"
        "```"
    ), inline=False)

    embed.add_field(name="**✚ Other**", value="n/help - Show this message", inline=False)
    embed.set_footer(text=f"Made by @captainn29 • Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# ------------------- Basic Commands -----------------------
@bot.command()
async def ping(ctx):
    await ctx.send(f"**🏓 [Pong! {round(bot.latency*1000)}ms]**")

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
        return await ctx.send(no_perm_msg("kick members"))
    try:
        await member.kick(reason=reason)
        await ctx.send(f"**✅ [User Kicked: {member}] Reason: {reason or 'No reason provided'}**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send(no_perm_msg("ban members"))
    try:
        await member.ban(reason=reason)
        await ctx.send(f"**✅ [User Banned: {member}] Reason: {reason or 'No reason provided'}**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def unban(ctx, user_id: int):
    if not ctx.author.guild_permissions.ban_members:
        return await ctx.send(no_perm_msg("unban members"))
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"**✅ [User Unbanned: {user}]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send(no_perm_msg("timeout members"))
    try:
        await member.timeout(timedelta(minutes=duration), reason=reason)
        await ctx.send(f"**✅ [User Timed Out: {member}] Duration: {duration} minutes**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def removetimeout(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send(no_perm_msg("remove timeouts"))
    try:
        await member.timeout(None)
        await ctx.send(f"**✅ [Timeout Removed: {member}]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send(no_perm_msg("warn users"))
    embed = discord.Embed(title="⚠️ Warning", description=f"{member.mention} has been warned!", color=discord.Color.red())
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Warned by", value=ctx.author.mention)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)
    try:
        await member.send(f"**⚠️ [You have been warned in {ctx.guild.name}.] Reason: {reason or 'No reason provided'}**")
    except:
        await ctx.send("**⚠️ [Warning sent, but user’s DMs are closed.]**")

# ------------------- Mute/Unmute -----------------------
@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send(no_perm_msg("mute users"))
    try:
        await member.timeout(timedelta(days=28), reason=reason)
        await ctx.send(f"**🔇 [User Muted: {member}]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def unmute(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.moderate_members:
        return await ctx.send(no_perm_msg("unmute users"))
    try:
        await member.timeout(None)
        await ctx.send(f"**🔊 [User Unmuted: {member}]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")
# ------------------- Clear Command -----------------------
@bot.command()
async def clear(ctx, amount: int, *args):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send(no_perm_msg("clear messages"))
    if amount < 1 or amount > 100:
        return await ctx.send("**❌ [Amount must be between 1–100]**")

    target_member = None
    only_images = False
    exclude_images = False

    mention_re = re.compile(r"<@!?(?P<id>\d+)>")
    args = list(args)
    i = 0
    while i < len(args):
        token = args[i]
        low = token.lower()
        if low.startswith("ex:") and len(low) > 3:
            rest = low[3:].strip()
            if rest in ("images", "image", "attachments", "attachment", "imgs"):
                exclude_images = True
            i += 1
            continue
        if low == "ex:":
            if i + 1 < len(args):
                nxt = args[i+1].lower()
                if nxt in ("images", "image", "attachments", "attachment", "imgs"):
                    exclude_images = True
                    i += 2
                    continue
            i += 1
            continue
        if low in ("images", "image", "attachments", "attachment", "imgs"):
            only_images = True
            i += 1
            continue
        m = mention_re.match(token)
        if m:
            uid = int(m.group("id"))
            mbr = ctx.guild.get_member(uid)
            if mbr:
                target_member = mbr
            i += 1
            continue
        i += 1

    def check(message):
        if message.id == ctx.message.id:
            return False
        if target_member and message.author.id != target_member.id:
            return False
        has_attachment = len(message.attachments) > 0
        if only_images and not has_attachment:
            return False
        if exclude_images and has_attachment:
            return False
        return True

    try:
        deleted = await ctx.channel.purge(limit=amount+1, check=check)
        deleted_count = len(deleted)
        await ctx.send(f"**✅ [Deleted {deleted_count} messages]**")
        await asyncio.sleep(3)
        try:
            await ctx.channel.purge(limit=5, check=lambda m: m.author == bot.user and m.content.startswith("**✅ [Deleted"))
        except:
            pass
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

# ------------------- Channel Commands -----------------------
@bot.command()
async def slowmode(ctx, seconds: int):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send(no_perm_msg("change slowmode"))
    if seconds < 0 or seconds > 21600:
        return await ctx.send("**❌ [Slowmode must be 0–21600 seconds]**")
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"**✅ [Slowmode set to {seconds} seconds]**" if seconds else "**✅ [Slowmode disabled]**")

@bot.command()
async def lock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send(no_perm_msg("lock the channel"))
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("**🔒 [Channel Locked]**")

@bot.command()
async def unlock(ctx):
    if not ctx.author.guild_permissions.manage_channels:
        return await ctx.send(no_perm_msg("unlock the channel"))
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send("**🔓 [Channel Unlocked]**")

# ------------------- Roles Commands -----------------------
@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if not ctx.author.guild_permissions.manage_roles:
        return await ctx.send(no_perm_msg("add roles"))
    try:
        await member.add_roles(role)
        await ctx.send(f"**✅ [Added {role.mention} to {member.mention}]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if not ctx.author.guild_permissions.manage_roles:
        return await ctx.send(no_perm_msg("remove roles"))
    try:
        await member.remove_roles(role)
        await ctx.send(f"**✅ [Removed {role.mention} from {member.mention}]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

@bot.command()
async def rolecatalog(ctx):
    roles = sorted(ctx.guild.roles[1:], key=lambda r: r.position, reverse=True)
    embed = discord.Embed(title=f"📘 Role Catalog - {ctx.guild.name}",
                          description=f"Total Roles: **{len(roles)}**",
                          color=discord.Color.orange())
    for role in roles:
        embed.add_field(name=role.name,
                        value=f"🆔 {role.id} | 👥 {len(role.members)} members",
                        inline=False)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

# ------------------- Info Commands -----------------------
@bot.command()
async def userinfo(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.purple())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Nickname", value=member.nick or "None")
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown")
    embed.add_field(name="Roles", value=", ".join([r.mention for r in member.roles[1:]]) or "None")
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.purple())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown")
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
async def serverbanner(ctx):
    if ctx.guild.banner:
        await ctx.send(ctx.guild.banner.url)
    else:
        await ctx.send("**❌ [This server has no banner]**")

@bot.command()
async def avatar(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.purple())
    embed.set_image(url=member.display_avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
async def time(ctx):
    await ctx.send(f"**⏰ [Current UTC Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}]**")

# ------------------- Fun Commands -----------------------
@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"**🤗 [{ctx.author.mention} hugged {member.mention}]**")

@bot.command()
async def hugall(ctx):
    await ctx.send(f"**🤗 [{ctx.author.mention} sends hugs to everyone]**")

@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"**💋 [{ctx.author.mention} kissed {member.mention}]**")

@bot.command()
async def flipcoin(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"**🪙 [The coin landed on {result}]**")

@bot.command()
async def roll(ctx, arg: Optional[str] = None):
    try:
        if arg is None:
            sides = 6
            result = random.randint(1, sides)
            await ctx.send(f"**🎲 [You rolled a {result} on a {sides}-sided die]**")
            return
        dice_match = re.match(r"^(\d+)d(\d+)$", arg.lower().strip())
        if dice_match:
            rolls = int(dice_match.group(1))
            sides = int(dice_match.group(2))
            if rolls < 1 or sides < 2:
                return await ctx.send("**❌ [Invalid dice. Example: 2d6]**")
            if rolls > 50:
                return await ctx.send("**❌ [Too many dice (max 50)]**")
            results = [random.randint(1, sides) for _ in range(rolls)]
            total = sum(results)
            await ctx.send(f"**🎲 [You rolled {', '.join(map(str, results))} → Total: {total} on {rolls}d{sides}]**")
            return
        else:
            sides = int(arg)
            if sides < 2:
                return await ctx.send("**❌ [Minimum sides is 2]**")
            result = random.randint(1, sides)
            await ctx.send(f"**🎲 [You rolled a {result} on a {sides}-sided die]**")
    except ValueError:
        await ctx.send("**❌ [Invalid argument. Use n/roll, n/roll XdY, or n/roll <sides>]**")
    except Exception as e:
        await ctx.send(f"**❌ [Error: {e}]**")

# ------------------- Poll & Announce -----------------------
DURATION_TOKEN_RE = re.compile(r"^(\d+)([wdhm])$")

def parse_duration_tokens(tokens):
    total_seconds = 0
    for t in tokens:
        m = DURATION_TOKEN_RE.match(t.lower())
        if not m:
            continue
        val = int(m.group(1))
        unit = m.group(2)
        if unit == 'w':
            total_seconds += val * 7 * 24 * 3600
        elif unit == 'd':
            total_seconds += val * 24 * 3600
        elif unit == 'h':
            total_seconds += val * 3600
        elif unit == 'm':
            total_seconds += val * 60
    return total_seconds

async def poll_timer(message, channel, duration_seconds, options, author):
    try:
        await asyncio.sleep(duration_seconds)
        try:
            msg = await channel.fetch_message(message.id)
        except Exception:
            await channel.send(f"**❌ [Poll could not be found or was deleted.]**")
            return

        reactions = msg.reactions[:len(options)]
        results = []
        for r in reactions:
            results.append(max(0, r.count - 1))

        total_votes = sum(results)
        if total_votes == 0:
            await channel.send(f"**✅ [Poll ended! No votes were cast.]**")
            return

        max_votes = max(results)
        winners = [options[i] for i, v in enumerate(results) if v == max_votes]
        if len(winners) == 1:
            winner_text = f"**{winners[0]}** with {max_votes} votes"
        else:
            winner_text = f"**Tie between: {', '.join(winners)}** with {max_votes} votes each"

        details = "\n".join([f"{i+1}. {options[i]} — {results[i]} votes" for i in range(len(options))])
        await channel.send(f"**✅ [Poll ended! Winner: {winner_text}]**\n**[Total votes: {total_votes}]**\n{details}\n( Poll created by {author.mention} )")
    except Exception as e:
        try:
            await channel.send(f"**❌ [Poll ended with error: {e}]**")
        except:
            pass

@bot.command()
async def poll(ctx, question: str, *options):
    if len(options) < 2:
        return await ctx.send("**❌ [Minimum 2 options required]**")
    options = list(options)
    duration_tokens = []
    while options and DURATION_TOKEN_RE.match(options[-1].lower()):
        duration_tokens.insert(0, options.pop())
    if duration_tokens:
        duration_seconds = parse_duration_tokens(duration_tokens)
        if duration_seconds <= 0:
            return await ctx.send("**❌ [Invalid duration specified]**")
    else:
        duration_seconds = 24 * 3600
    if len(options) > 10:
        return await ctx.send("**❌ [Maximum 10 options allowed]**")
    reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    description = "\n".join([f"{reactions[i]} {opt}" for i,opt in enumerate(options)])
    embed = discord.Embed(title=f"📊 {question}", description=description, color=discord.Color.gold())
    embed.set_footer(text=f"Poll by {ctx.author} • Ends in {(' '.join(duration_tokens)) if duration_tokens else '24h (default)'}")
    poll_message = await ctx.send(embed=embed)
    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])
    asyncio.create_task(poll_timer(poll_message, ctx.channel, duration_seconds, options, ctx.author))

@bot.command()
async def announce(ctx, *, message: str):
    if not ctx.author.guild_permissions.manage_messages:
        return await ctx.send(no_perm_msg("make announcements"))
    embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
    embed.set_footer(text=f"**Announcements** • Requested by {ctx.author}")
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(embed=embed)

# ------------------- Status Command -----------------------
@bot.command()
async def status(ctx):
    try:
        now = datetime.utcnow()
        uptime_delta = now - bot_start_time
        days, remainder = divmod(uptime_delta.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m"

        latency = round(bot.latency * 1000)
        guild_count = len(bot.guilds)
        user_count = sum(g.member_count for g in bot.guilds)

        render_url = "https://nexus-02-5.onrender.com"
        web_status = "❌ Offline"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(render_url, timeout=5) as resp:
                    if resp.status == 200:
                        web_status = "✅ Online"
            except:
                web_status = "❌ Offline"

        embed = discord.Embed(
            title="**🛰️ [Bot Status]**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Uptime", value=f"**[{uptime_str}]**", inline=False)
        embed.add_field(name="Ping", value=f"**[{latency}ms]**", inline=False)
        embed.add_field(name="Servers | Users", value=f"**[{guild_count} | {user_count}]**", inline=False)
        embed.add_field(name="Web Service", value=f"**[{web_status}]**", inline=False)
        embed.set_footer(text=f"Last Reboot: {bot_start_time.strftime('%Y-%m-%d %H:%M UTC')} • Requested by {ctx.author}")

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"**❌ [Error fetching status: {e}]**")

# ------------------- Run Bot -------------------------------
token = os.environ.get("DISCORD_TOKEN")
if not token:
    print("❌ Please set your DISCORD_TOKEN environment variable!")
else:
    bot.run(token)        
