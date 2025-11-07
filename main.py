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
from discord.ext import commands
import discord
from datetime import datetime, timezone

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="n/", intents=intents, help_command=None)

bot_start_time = datetime.now(timezone.utc)

# ------------------- Helper -----------------------
def no_perm_msg(action):
    return f"**❌ [You do not have permission to {action}]**"

# ------------------- Events -----------------------
@bot.event
async def on_ready():
    print(f"✅ [Logged in as {bot.user}]")

# -------------------- HELP COMMAND --------------------
from discord.ui import View, Button
import discord

@bot.command(name="help")
async def help_command(ctx):
    # === PAGE 1: Nexus Cover ===
    cover = discord.Embed(color=discord.Color.gold())
    cover.set_image(url="https://cdn.discordapp.com/attachments/1421960903603130580/1436434756014309537/image.jpg?ex=690f979d&is=690e461d&hm=c1ddcbd8c6fab9dd0d481a6ea1d30d77f36214ee953e80c08772a4a487c2b5ec&")
    cover.set_footer(text="𝐍𝐞𝐱𝐮𝐬 𝐁𝐨𝐭 • 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐈𝐧𝐝𝐞𝐱")

    # === PAGE 2: Moderation ===
    mod = discord.Embed(title="⛊ **Moderation**", color=discord.Color.blue())
    mod.description = (
        "**n/kick @user <reason>** - Kick a member\n"
        "**n/ban @user <reason>** - Ban a member\n"
        "**n/unban <user_id>** - Unban a user\n"
        "**n/timeout @user <minutes> [reason]** - Timeout a member\n"
        "**n/removetimeout @user** - Remove a timeout\n"
        "**n/mute @user [reason]** - Mute a member\n"
        "**n/unmute @user** - Unmute a member\n"
        "**n/warn @user [reason]** - Warn a member\n"
        "**n/snipe [0-5] [#channel]** - Retrieve deleted messages\n"
        "**n/clear <amount> [images/users]** - Clear messages"
    )

    # === PAGE 3: Channel ===
    channel = discord.Embed(title="⚙︎ **Channel**", color=discord.Color.blue())
    channel.description = (
        "**n/slowmode <seconds>** - Set slowmode delay\n"
        "**n/lock** - Lock the channel\n"
        "**n/unlock** - Unlock the channel"
    )

    # === PAGE 4: Roles ===
    roles = discord.Embed(title="𐀪 **Roles**", color=discord.Color.blue())
    roles.description = (
        "**n/addrole @user @role** - Give a role\n"
        "**n/removerole @user @role** - Remove a role\n"
        "**n/rolecatalog** - View all roles"
    )

    # === PAGE 5: Info ===
    info = discord.Embed(title="𝒊 **Info**", color=discord.Color.blue())
    info.description = (
        "**n/userinfo @user** - View user info\n"
        "**n/serverinfo** - Server info\n"
        "**n/serverbanner** - Server banner\n"
        "**n/avatar @user** - User avatar\n"
        "**n/ping** - Bot latency\n"
        "**n/time** - Current UTC time\n"
        "**n/status** - Bot & web status\n"
        "**n/invite** - Invite link"
    )

    # === PAGE 6: Fun & Utility ===
    fun = discord.Embed(title="☻ **Fun & Utility**", color=discord.Color.blue())
    fun.description = (
        "**n/say <message>** - Repeat your message\n"
        "**n/poll \"question\" <option1> <option2> [0d 0h]** - Start a poll\n"
        "**n/announce <message>** - Announce message\n"
        "**n/hug @user** - Hug someone\n"
        "**n/hugall** - Hug everyone\n"
        "**n/kiss @user** - Kiss someone\n"
        "**n/flipcoin** - Flip a coin\n"
        "**n/roll [sides]** or **XdY** - Roll dice\n"
        "**n/8ball <question>** - Magic 8ball\n"
        "**n/meme** - Random meme\n"
        "**n/rps <rock/paper/scissors>** - Play RPS\n"
        "**n/tictactoe @opponent** - Tic Tac Toe\n"
        "**n/tttmove <1-9>** - Move in Tic Tac Toe\n"
        "**n/connect4 @opponent** - Connect 4\n"
        "**n/c4move <1-7>** - Connect 4 move\n"
        "**n/rpg** - Interactive text RPG\n"
        "**n/spellduel @opponent** - Spell duel\n"
        "**n/rapbattle @opponent** - Rap battle\n"
        "**n/wordchain** - Word chain game\n"
        "**n/endwordchain** - End word chain"
    )

    # === PAGE 7: Other ===
    other = discord.Embed(title="✚ **Other**", color=discord.Color.blue())
    other.description = "**n/help** - Show this message"

    # === PAGE SYSTEM ===
    pages = [cover, mod, channel, roles, info, fun, other]
    current = 0

    view = View(timeout=360)  # 6-minute timeout

    # Navigation Buttons
    back = Button(label="Previous", style=discord.ButtonStyle.secondary)
    next = Button(label="Next", style=discord.ButtonStyle.secondary)

    async def update_page(interaction):
        await interaction.response.edit_message(embed=pages[current], view=view)

    async def next_callback(interaction):
        nonlocal current
        if current < len(pages) - 1:
    current += 1
await update_page(interaction)

        await update_page(interaction)

    async def back_callback(interaction):
        nonlocal current
        if current > 0:
    current -= 1
await update_page(interaction)

        await update_page(interaction)

    next.callback = next_callback
    back.callback = back_callback

    view.add_item(back)
    view.add_item(next)

    await ctx.send(embed=pages[current], view=view)
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

# ------------------- Advanced Snipe Command -----------------------
from collections import defaultdict

# Store deleted messages per channel (up to 10 per channel)
snipes = defaultdict(list)

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    # Get first attachment URL if any
    attachment_url = message.attachments[0].url if message.attachments else None

    snipes[message.channel.id].insert(0, {
        "content": message.content if message.content else "[Attachment]",
        "author": message.author,
        "time": datetime.utcnow(),
        "attachment": attachment_url
    })

    # Keep only last 10 deletions per channel
    if len(snipes[message.channel.id]) > 10:
        snipes[message.channel.id].pop()

@bot.command()
async def snipe(ctx, index: int = 1, channel: discord.TextChannel = None):
    """
    Usage:
    n/snipe               -> Last deleted message in current channel
    n/snipe 3             -> 3rd last deleted message in current channel
    n/snipe 2 #general    -> 2nd last deleted message in #general
    """

    channel = channel or ctx.channel
    messages = snipes.get(channel.id)

    if not messages:
        return await ctx.send(f"**❌ [No recently deleted messages found in {channel.mention}]**")

    if index < 1 or index > len(messages):
        return await ctx.send(f"**❌ [There are only {len(messages)} deleted messages stored for {channel.mention}]**")

    data = messages[index - 1]
    author = data["author"]
    content = data["content"]
    attachment = data["attachment"]
    time_deleted = data["time"].strftime("%Y-%m-%d %H:%M:%S UTC")

    embed = discord.Embed(description=content, color=discord.Color.red())
    embed.set_author(name=f"{author} said in #{channel.name}:")
    embed.set_footer(text=f"Deleted at {time_deleted} • Requested by {ctx.author}")

    if attachment:
        embed.set_image(url=attachment)

    await ctx.send(embed=embed)

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
    embed.add_field(name="Channels & Categories", value=len(guild.channels))
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

@bot.command()
async def invite(ctx):
    app_info = await bot.application_info()
    invite_link = f"https://discord.com/oauth2/authorize?client_id={app_info.id}&permissions=8&scope=bot%20applications.commands"
    await ctx.send(f"**🔗 [[Click here](https://discord.com/oauth2/authorize?client_id=1432139270860177581&permissions=8&integration_type=0&scope=bot) to invite 𝐍𝐞𝐱𝐮𝐬 bot to your server.]**")

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

@bot.command(aliases=['8ball'])
async def eightball(ctx, *, question: str):
    responses = [
        "It is certain.", "Without a doubt.", "You may rely on it.",
        "Yes, definitely.", "As I see it, yes.", "Most likely.",
        "Outlook good.", "Signs point to yes.", "Reply hazy, try again.",
        "Ask again later.", "Better not tell you now.",
        "Cannot predict now.", "Concentrate and ask again.",
        "Don’t count on it.", "My reply is no.",
        "Outlook not so good.", "Very doubtful."
    ]
    await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {random.choice(responses)}")

from discord.ext import commands
import aiohttp, asyncio, random, discord

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(name="meme")
async def meme(ctx):
    """Fetch a random meme from meme-api.com (with cooldown)"""
    async with aiohttp.ClientSession() as session:
        try:
            # Fetch meme from API
            async with session.get(
                "https://meme-api.com/gimme",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status != 200:
                    raise Exception(f"Bad response: {resp.status}")

                data = await resp.json()
                title = data.get("title", "Random Meme")
                subreddit = data.get("subreddit", "unknown")
                post_url = data.get("postLink", "")
                image_url = data.get("url")

                embed = discord.Embed(
                    title=f"😂 {title}",
                    url=post_url,
                    color=discord.Color.random()
                )
                embed.set_image(url=image_url)
                embed.set_footer(
                    text=f"From r/{subreddit} • Requested by {ctx.author.display_name}"
                )

                await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send("⏰ **[The meme API took too long to respond! Try again soon]**")

        except aiohttp.ClientError as e:
            await ctx.send(f"🌐 **[Network error while fetching meme: `{e}` ]**")

        except Exception:
            # Fallback meme if API fails
            fallback_memes = [
                "https://i.redd.it/q9l8tlfp6ik71.jpg",
                "https://i.imgur.com/fY4dWUz.jpeg",
                "https://i.redd.it/z3hr7s3klpm81.jpg"
            ]
            embed = discord.Embed(
                title="😂 Meme API failed — here’s a backup meme!",
                color=discord.Color.orange()
            )
            embed.set_image(url=random.choice(fallback_memes))
            await ctx.send(embed=embed)


@meme.error
async def meme_error(ctx, error):
    """Handle cooldown errors nicely"""
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"🕒 **[Slow down {ctx.author.mention}! Try again in `{error.retry_after:.1f}` seconds]**"
        )

@bot.command()
async def rps(ctx, choice: str):
    """Play Rock-Paper-Scissors"""
    choices = ["rock", "paper", "scissors"]
    choice = choice.lower()
    if choice not in choices:
        return await ctx.send("❌ **[Choose rock, paper, or scissors!]**")

    bot_choice = random.choice(choices)
    if choice == bot_choice:
        result = "It's a tie!"
    elif (choice == "rock" and bot_choice == "scissors") or \
         (choice == "paper" and bot_choice == "rock") or \
         (choice == "scissors" and bot_choice == "paper"):
        result = "You win!"
    else:
        result = "You lose!"

    await ctx.send(f"🤖 **[I chose **{bot_choice}**.\n🎉 {result} ]**")

active_ttt = {}

@bot.command()
async def tictactoe(ctx, opponent: discord.Member):
    """Play Tic-Tac-Toe with another user"""
    if ctx.channel.id in active_ttt:
        return await ctx.send("❌ A game is already active in this channel.")

    board = ["⬜"] * 9
    turn = ctx.author
    active_ttt[ctx.channel.id] = {"board": board, "turn": turn, "player1": ctx.author, "player2": opponent}

    def format_board(b):
        return f"{b[0]}{b[1]}{b[2]}\n{b[3]}{b[4]}{b[5]}\n{b[6]}{b[7]}{b[8]}"

    await ctx.send(f"🎮 **[Tic-Tac-Toe started! {ctx.author.mention} vs {opponent.mention} ]**\n\n{format_board(board)}\nIt's {turn.mention}'s turn!] Pick a position 1-9 with `n/tttmove <pos>`")

@bot.command()
async def tttmove(ctx, pos: int):
    """Make a move in Tic-Tac-Toe"""
    game = active_ttt.get(ctx.channel.id)
    if not game:
        return await ctx.send("❌ **[No active game here]**")
    if ctx.author != game["turn"]:
        return await ctx.send("❌ **[It's not your turn]**")
    if pos < 1 or pos > 9:
        return await ctx.send("❌ **[Position must be 1-9]**")
    board = game["board"]
    if board[pos-1] != "⬜":
        return await ctx.send("❌ **[That spot is already taken]**")

    mark = "❌" if ctx.author == game["player1"] else "⭕"
    board[pos-1] = mark

    def check_win(b, m):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(b[i]==b[j]==b[k]==m for i,j,k in wins)

    def format_board(b):
        return f"{b[0]}{b[1]}{b[2]}\n{b[3]}{b[4]}{b[5]}\n{b[6]}{b[7]}{b[8]}"

    if check_win(board, mark):
        await ctx.send(f"{format_board(board)}\n🎉 {ctx.author.mention} wins!")
        active_ttt.pop(ctx.channel.id)
        return
    if "⬜" not in board:
        await ctx.send(f"{format_board(board)}\n🤝 It's a tie!")
        active_ttt.pop(ctx.channel.id)
        return

    game["turn"] = game["player2"] if game["turn"] == game["player1"] else game["player1"]
    await ctx.send(f"{format_board(board)}\nIt's {game['turn'].mention}'s turn!")

active_c4 = {}

ROWS, COLS = 6, 7

@bot.command()
async def connect4(ctx, opponent: discord.Member):
    """Start Connect 4"""
    if ctx.channel.id in active_c4:
        return await ctx.send("❌ **[A Connect 4 game is already active here]**")

    board = [["⚪" for _ in range(COLS)] for _ in range(ROWS)]
    turn = ctx.author
    active_c4[ctx.channel.id] = {"board": board, "turn": turn, "player1": ctx.author, "player2": opponent}

    def format_board(b):
        s = ""
        for row in b:
            s += "".join(row) + "\n"
        s += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
        return s

    await ctx.send(f"🎮 **[Connect 4 started!]** {ctx.author.mention} vs {opponent.mention}\n\n{format_board(board)}\nUse `n/c4move <column>` to play!")

@bot.command()
async def c4move(ctx, col: int):
    """Make a move in Connect 4"""
    game = active_c4.get(ctx.channel.id)
    if not game:
        return await ctx.send("❌ **[No active Connect 4 game]**")
    if ctx.author != game["turn"]:
        return await ctx.send("❌ **[It's not your turn]**")
    if not 1 <= col <= COLS:
        return await ctx.send("❌ **[Column must be 1-7]**")

    board = game["board"]
    col -= 1
    for row in reversed(board):
        if row[col] == "⚪":
            row[col] = "🔴" if ctx.author == game["player1"] else "🟡"
            break
    else:
        return await ctx.send("❌ That column is full!")

    def check_win(b, piece):
        # horizontal, vertical, diagonal
        for r in range(ROWS):
            for c in range(COLS-3):
                if all(b[r][c+i]==piece for i in range(4)):
                    return True
        for r in range(ROWS-3):
            for c in range(COLS):
                if all(b[r+i][c]==piece for i in range(4)):
                    return True
        for r in range(ROWS-3):
            for c in range(COLS-3):
                if all(b[r+i][c+i]==piece for i in range(4)):
                    return True
        for r in range(3, ROWS):
            for c in range(COLS-3):
                if all(b[r-i][c+i]==piece for i in range(4)):
                    return True
        return False

    piece = "🔴" if ctx.author == game["player1"] else "🟡"
    def format_board(b):
        s = ""
        for row in b:
            s += "".join(row) + "\n"
        s += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
        return s

    if check_win(board, piece):
        await ctx.send(f"{format_board(board)}\n🎉 {ctx.author.mention} wins!")
        active_c4.pop(ctx.channel.id)
        return

    if all(board[0][c] != "⚪" for c in range(COLS)):
        await ctx.send(f"{format_board(board)}\n🤝 It's a tie!")
        active_c4.pop(ctx.channel.id)
        return

    game["turn"] = game["player2"] if game["turn"] == game["player1"] else game["player1"]
    await ctx.send(f"{format_board(board)}\nIt's {game['turn'].mention}'s turn!")

import random
import asyncio

# Track active adventures
active_adventures = {}
player_stats = {}

# Adventure rooms with branching paths and multiple endings
adventure_rooms = {
    "start": {
        "desc": "🗺️ You find yourself in a mysterious forest. Two paths lie ahead: `left` or `right`?",
        "choices": {"left": "river", "right": "cave"}
    },
    "river": {
        "desc": "🌊 A wide river blocks your way. Do you `swim` across or `walk` along the bank?",
        "choices": {"swim": "shark", "walk": "hut"}
    },
    "cave": {
        "desc": "🕳️ You enter a dark cave. `explore` deeper or `exit` back?",
        "choices": {"explore": "treasure", "exit": "start"}
    },
    "shark": {
        "desc": "🦈 A shark attacks while you swim! You barely escape and reach a hut.",
        "choices": {"continue": "hut"}
    },
    "hut": {
        "desc": "🏠 You find a small hut with a friendly old man who offers a potion. Do you `take` it or `ignore` it?",
        "choices": {"take": "potion", "ignore": "forest_exit"}
    },
    "treasure": {
        "desc": "💰 You found a hidden treasure! 🎉 Congratulations, you win!",
        "choices": {}
    },
    "potion": {
        "desc": "🧪 The potion gives you magical strength! Do you continue `forward` or `rest`?",
        "choices": {"forward": "dragon_lair", "rest": "forest_exit"}
    },
    "dragon_lair": {
        "desc": "🐉 You encounter a sleeping dragon. Do you `fight` or `sneak` past it?",
        "choices": {"fight": "dragon_fight", "sneak": "forest_exit"}
    },
    "dragon_fight": {
        "desc": "⚔️ You bravely fight the dragon!",
        "choices": {}
    },
    "forest_exit": {
        "desc": "🌳 You safely exit the forest. Adventure complete! 🎉",
        "choices": {}
    }
}

# Define possible fight outcomes
async def dragon_fight_outcome(ctx, user):
    outcome = random.choice(["win", "lose"])
    if outcome == "win":
        await ctx.send("🎉 **[You slayed the dragon and found legendary treasure! You win!]**")
    else:
        await ctx.send("💀 **[The dragon overpowered you. You died.]**")
    active_adventures.pop(user.id)
    player_stats.pop(user.id)

# Command to start RPG
@bot.command(name="rpg")
async def mini_rpg(ctx):
    if ctx.author.id in active_adventures:
        return await ctx.send("❌ **[You already have an active adventure]**")

    active_adventures[ctx.author.id] = "start"
    player_stats[ctx.author.id] = {"hp": 100, "items": []}

    await ctx.send(f"Welcome {ctx.author.mention} to the Mini RPG!\nType your choices to play.\n")
    await show_room(ctx, ctx.author)

async def show_room(ctx, user):
    room_key = active_adventures[user.id]
    room = adventure_rooms[room_key]
    desc = room["desc"]
    choices = list(room["choices"].keys())
    
    choice_text = "\nChoices: " + ", ".join(f"`{c}`" for c in choices) if choices else "\nNo choices, adventure ends."
    await ctx.send(desc + choice_text)

    if not choices:
        # Special case for dragon fight
        if room_key == "dragon_fight":
            await dragon_fight_outcome(ctx, user)
        else:
            active_adventures.pop(user.id)
            player_stats.pop(user.id)
        return

    def check(m):
        return m.author == user and m.channel == ctx.channel and m.content.lower() in choices

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        choice = msg.content.lower()

        # Random encounter damage example
        if room_key == "river" and choice == "swim":
            damage = random.randint(5, 20)
            player_stats[user.id]["hp"] -= damage
            await ctx.send(f"💥 You struggled in the water and lost {damage} HP! Current HP: {player_stats[user.id]['hp']}")
            if player_stats[user.id]["hp"] <= 0:
                await ctx.send("💀 **[You Died. Adventure over.]**")
                active_adventures.pop(user.id)
                player_stats.pop(user.id)
                return

        # Move to next room
        next_room = room["choices"][choice]
        active_adventures[user.id] = next_room
        await show_room(ctx, user)
    except asyncio.TimeoutError:
        await ctx.send("⌛ **[Adventure timed out! Try again later.]**")
        active_adventures.pop(user.id)
        player_stats.pop(user.id)

active_spell_duels = {}

SPELLS = {
    "fireball": (20, "🔥 Fireball"),
    "iceblast": (15, "❄️ Ice Blast"),
    "lightning": (25, "⚡ Lightning Strike"),
    "heal": (-20, "💖 Heal")
}

@bot.command()
async def spellduel(ctx, member: discord.Member):
    if ctx.author.id in active_spell_duels or member.id in active_spell_duels:
        return await ctx.send("❌ **[One of you is already in a duel]**")
    
    hp = {ctx.author: 100, member: 100}
    turn_order = [ctx.author, member]
    current_turn = 0

    active_spell_duels[ctx.author.id] = member.id
    active_spell_duels[member.id] = ctx.author.id

    await ctx.send(f"🧙‍♂️ **[Spell Duel started: {ctx.author.mention} vs {member.mention} ]**\nEach player has 100 HP.\nAvailable spells: {', '.join(SPELLS.keys())}")

    while all(hp[p] > 0 for p in turn_order):
        player = turn_order[current_turn]
        opponent = turn_order[1-current_turn]

        await ctx.send(f"🎯 {player.mention}, it's your turn! Choose a spell: {', '.join(SPELLS.keys())}")

        def check(m):
            return m.author == player and m.channel == ctx.channel and m.content.lower() in SPELLS

        try:
            msg = await bot.wait_for('message', check=check, timeout=30)
            spell = msg.content.lower()
            dmg, name = SPELLS[spell]
            hp[opponent] -= dmg if dmg > 0 else 0
            if dmg < 0:
                hp[player] = min(100, hp[player]-dmg)  # heal
            await ctx.send(f"{player.mention} used {name}!\n{opponent.mention} HP: {hp[opponent]}\n{player.mention} HP: {hp[player]}")
        except asyncio.TimeoutError:
            await ctx.send(f"⌛ {player.mention} took too long! Skipping turn.")

        if hp[opponent] <= 0:
            await ctx.send(f"🎉 {player.mention} wins the duel!")
            break
        current_turn = 1 - current_turn

    active_spell_duels.pop(ctx.author.id, None)
    active_spell_duels.pop(member.id, None)

import asyncio
import discord
from discord.ext import commands

active_rapbattles = {}  # Track active rap battles per channel

@bot.command()
async def rapbattle(ctx, opponent: discord.Member):
    """Challenge a user to a rap battle."""
    if ctx.author.id == opponent.id:
        return await ctx.send("❌ **[You cannot rap battle yourself]**")
    
    if ctx.channel.id in active_rapbattles:
        return await ctx.send("❌ **[A rap battle is already active in this channel]**")

    # Send challenge embed
    embed = discord.Embed(
        title="🎤 **[Rap Battle Challenge!]**",
        description=f"{ctx.author.mention} has challenged {opponent.mention} to a rap battle!\nDo you accept?",
        color=discord.Color.purple()
    )
    embed.set_footer(text="React with ✅ to accept or ❌ to decline.")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    def check(reaction, user):
        return user == opponent and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

    try:
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=60)
    except asyncio.TimeoutError:
        return await ctx.send("⌛ **[Challenge timed out]**")

    if str(reaction.emoji) == "❌":
        return await ctx.send(f"❌ **[ {opponent.mention} declined the rap battle]**")

    # Start battle
    active_rapbattles[ctx.channel.id] = {
        "players": [ctx.author, opponent],
        "turn_index": 0,
        "lines": {ctx.author.id: [], opponent.id: []},
        "round": 1
    }

    await ctx.send(f"🔥 **[Rap battle started between {ctx.author.mention} (🔥) and {opponent.mention} (😎)!]**\nTake turns sending your rap lines. 3 rounds total.")
    await next_rap_turn(ctx)

async def next_rap_turn(ctx):
    battle = active_rapbattles[ctx.channel.id]
    players = battle["players"]
    turn_index = battle["turn_index"]
    player = players[turn_index]

    await ctx.send(f"🎤 **{player.display_name}'s turn!** Send your rap line now.")

    def check_msg(m):
        return m.author == player and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check_msg, timeout=120)
        battle["lines"][player.id].append(msg.content)
    except asyncio.TimeoutError:
        await ctx.send(f"⌛ **[ {player.mention} took too long! Skipping turn]**")
        battle["lines"][player.id].append("...")  # Empty line

    # Switch turn
    battle["turn_index"] = 1 - turn_index
    # Increment round every 2 turns
    if battle["turn_index"] == 0:
        battle["round"] += 1

    if battle["round"] > 3:
        # Battle ends
        await end_rapbattle(ctx)
    else:
        await next_rap_turn(ctx)

async def end_rapbattle(ctx):
    battle = active_rapbattles.pop(ctx.channel.id)
    p1, p2 = battle["players"]
    p1_lines = battle["lines"][p1.id]
    p2_lines = battle["lines"][p2.id]

    embed = discord.Embed(
        title="🎤 **[Rap Battle Ended! Time to vote!]**",
        description="React with 🔥 for **Player 1** or 😎 for **Player 2**",
        color=discord.Color.gold()
    )

    battle_text = ""
    for i in range(len(p1_lines)):
        battle_text += f"**Round {i+1}**\n(🔥) **[{p1.display_name}]:** {p1_lines[i]}\n(😎) **[{p2.display_name}]:** {p2_lines[i]}\n\n"

    embed.add_field(name="Rap Battle Lines", value=battle_text[:1024])  # Discord field limit
    vote_msg = await ctx.send(embed=embed)
    await vote_msg.add_reaction("🔥")
    await vote_msg.add_reaction("😎")

    await asyncio.sleep(30)  # Voting time
    vote_msg = await ctx.channel.fetch_message(vote_msg.id)

    votes_p1 = next((r.count - 1 for r in vote_msg.reactions if str(r.emoji) == "🔥"), 0)
    votes_p2 = next((r.count - 1 for r in vote_msg.reactions if str(r.emoji) == "😎"), 0)

    winner_text = f"(🔥) **[{p1.display_name}]: {votes_p1} votes**\n(😎) **[{p2.display_name}]: {votes_p2} votes**"
    if votes_p1 > votes_p2:
        winner = p1.display_name
    elif votes_p2 > votes_p1:
        winner = p2.display_name
    else:
        winner = "Tie!"

    await ctx.send(f"🏆 **[The rap battle winner is: **{winner}**!\n{winner_text} ]**")

import asyncio
import aiohttp
import discord
from discord.ext import commands

# Enable the default intents and the message content intent
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent to read messages

# Create the bot with your custom prefix "n/"
bot = commands.Bot(command_prefix="n/", intents=intents)


# Track active games per channel
active_wordchain = {}


async def is_valid_english_word(word: str) -> bool:
    """Check if a word exists in the English dictionary using the Free Dictionary API."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return isinstance(data, list) and "word" in data[0]
            return False


def number_to_emoji(num: int) -> str:
    """Convert a number into emoji digits (e.g. 123 -> 1️⃣2️⃣3️⃣)."""
    emoji_map = {
        "0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"
    }
    return "".join(emoji_map.get(d, d) for d in str(num))


@bot.command(name="wordchain")
async def wordchain(ctx, starting_word: str):
    """Start a never-ending word chain game."""
    channel = ctx.channel

    if channel.id in active_wordchain:
        await ctx.send("⚠️ **[A word chain is already running in this channel]**")
        return

    # Validate starting word
    if not await is_valid_english_word(starting_word):
        await ctx.send(f"❌ '{starting_word}' is not a valid English word.")
        return

    active_wordchain[channel.id] = {
        "current_word": starting_word.lower(),
        "last_user": ctx.author.id,
        "chain_length": 0,
        "first_message_done": False
    }

    await ctx.send(
        f"🔤 **Word Chain Started!**\n"
        f"Starting word: **{starting_word}**\n"
        f"Next word must start with **{starting_word[-1].upper()}**!"
    )

    def check(msg):
        return (
            msg.channel == channel
            and not msg.author.bot
            and msg.content.isalpha()  # only allow alphabetic words
        )

    while True:
        try:
            msg = await bot.wait_for("message", check=check)
            word = msg.content.lower()

            game = active_wordchain.get(channel.id)
            if not game:
                break  # game manually ended

            last_word = game["current_word"]
            last_user = game["last_user"]

            # Prevent same user twice
            if msg.author.id == last_user:
                await channel.send(f"🚫 **[ {msg.author.mention}, you can’t play twice in a row]**")
                continue

            # Check first letter rule
            if word[0] != last_word[-1]:
                await channel.send(
                    f"❌ **[ {msg.author.mention} broke the chain]**\n"
                    f"Word must start with **{last_word[-1].upper()}**."
                )
                del active_wordchain[channel.id]
                break

            # Validate dictionary
            if not await is_valid_english_word(word):
                await channel.send(f"📘 **[ {msg.author.mention}, '{word}' is not a valid English word]**")
                continue

            # ✅ Valid move
            game["current_word"] = word
            game["last_user"] = msg.author.id
            game["chain_length"] += 1

            # React with emoji digits
            chain_num = game["chain_length"]
            for digit_emoji in number_to_emoji(chain_num):
                await msg.add_reaction(digit_emoji)

            # First message shows next letter, later ones just “accepted”
            if not game["first_message_done"]:
                await channel.send(
                    f"✅ **{word.capitalize()}** accepted! Next word must start with **{word[-1].upper()}**."
                )
                game["first_message_done"] = True
            else:
                await channel.send(f"✅ **{word.capitalize()}** accepted!")

        except Exception as e:
            await channel.send(f"⚠️ **[Error: `{e}`]**")
            break


@bot.command(name="endwordchain")
@commands.has_permissions(manage_messages=True)
async def endwordchain(ctx):
    """Manually end an ongoing word chain game."""
    channel = ctx.channel
    if channel.id not in active_wordchain:
        await ctx.send("❌ **[No active word chain in this channel]**")
        return

    del active_wordchain[channel.id]
    await ctx.send("🛑 **[The word chain has been ended by a moderator]**")

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
    embed = discord.Embed(title="📢 **Announcement**", description=message, color=discord.Color.gold())
    embed.set_footer(text=f"Announcements • Requested by {ctx.author}")
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(embed=embed)

# ------------------- Owner-only Command: List Servers -----------------------
@bot.command()
async def servers(ctx):
    OWNER_ID = 1210700638904656027  # 👑 Your Discord user ID

    # Only allow you (the owner) to use this command
    if ctx.author.id != OWNER_ID:
        return await ctx.send("**❌ [You do not have permission to use this command]**")

    # Create a list of servers with name, ID, and member count
    guild_list = [
        f"{guild.name} — 👥 {guild.member_count} members (ID: {guild.id})"
        for guild in bot.guilds
    ]
    guild_text = "\n".join(guild_list)

    # Handle empty or long outputs
    if not guild_list:
        guild_text = "I'm not in any servers yet!"
    elif len(guild_text) > 1900:
        guild_text = guild_text[:1900] + "\n... (list truncated)"

    # Try to send the server list in your DMs
    try:
        await ctx.author.send(f"📋 **Servers I'm in:**\n{guild_text}")
        await ctx.send("✅ **[I've sent you a DM with the server list]**")
    except discord.Forbidden:
        await ctx.send("⚠️ **[I couldn't DM you — please enable DMs from server members]**")

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
                        web_status = "✅ **[Online]**"
            except:
                web_status = "❌ **[Offline]**"

        embed = discord.Embed(
            title="**🛰️ [Bot Status]**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Uptime", value=f"**[{uptime_str}]**", inline=False)
        embed.add_field(name="Ping", value=f"**[{latency}ms]**", inline=False)
        embed.add_field(name="Servers | Users", value=f"**[{guild_count} | {user_count}]**", inline=False)
        embed.add_field(name="Web Service", value=web_status, inline=False)
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
