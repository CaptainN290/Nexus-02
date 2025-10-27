# At the very top of your bot's main file (e.g., main.py or bot.py)
import os
import threading
from flask import Flask

# ---- Flask setup ----
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    # Render sets PORT automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Start Flask in a separate thread so it doesn’t block your bot
threading.Thread(target=run_flask).start()
# ----------------------

import os
import discord
from discord.ext import commands
from typing import Optional

# Bot setup with secure token handling
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="n/", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def help(ctx):
    """Shows all available commands."""
    embed = discord.Embed(
        title="🤖 Nexus Bot - Command List",
        description="Complete list of all available commands",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🛡️ Moderation Commands",
        value=(
            "`n/kick @user <reason>` - Kick a member\n"
            "`n/ban @user <reason>` - Ban a member\n"
            "`n/unban <user_id> <reason>` - Unban a user\n"
            "`n/timeout @user <minutes> <reason>` - Timeout a member\n"
            "`n/warn @user <reason>` - Warn a member\n"
            "`n/mute @user <reason>` - Mute a member\n"
            "`n/unmute @user` - Unmute a member\n"
            "`n/clear <amount>` - Delete messages (1-100)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 Channel Management",
        value=(
            "`n/slowmode <seconds>` - Set slowmode (0-21600s)\n"
            "`n/lock` - Lock the channel\n"
            "`n/unlock` - Unlock the channel"
        ),
        inline=False
    )
    
    embed.add_field(
        name="👥 Role Management",
        value=(
            "`n/addrole @user @role` - Add a role to a user\n"
            "`n/removerole @user @role` - Remove a role from a user"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Information Commands",
        value=(
            "`n/userinfo [@user]` - Show user information\n"
            "`n/serverinfo` - Show server information\n"
            "`n/avatar [@user]` - Show user's avatar\n"
            "`n/ping` - Check bot latency"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎉 Fun & Utility",
        value=(
            "`n/say <message>` - Make the bot say something\n"
            '`n/poll "question" option1 option2...` - Create a poll\n'
            "`n/announce <message>` - Send an announcement"
        ),
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Other",
        value="`n/help` - Show this message",
        inline=False
    )
    
    embed.set_footer(text="Nexus Bot | Your Complete Moderation Solution")
    
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, message: str):
    """Bot repeats the message you type after the command."""
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass
    await ctx.send(message)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kicks a member from the server."""
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ You don't have permission to kick members!")
        return
    
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason or 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to kick this member!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bans a member from the server."""
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ You don't have permission to ban members!")
        return
    
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} has been banned. Reason: {reason or 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to ban this member!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    """Times out a member for a specified number of minutes."""
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ You don't have permission to timeout members!")
        return
    
    try:
        from datetime import timedelta
        timeout_duration = timedelta(minutes=duration)
        await member.timeout(timeout_duration, reason=reason)
        await ctx.send(f"✅ {member.mention} has been timed out for {duration} minutes. Reason: {reason or 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to timeout this member!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def unban(ctx, user_id: int, *, reason=None):
    """Unbans a user by their ID."""
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ You don't have permission to unban members!")
        return
    
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"✅ {user.name} has been unbanned. Reason: {reason or 'No reason provided'}")
    except discord.NotFound:
        await ctx.send("❌ User not found or not banned!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to unban users!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    """Warns a member."""
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ You don't have permission to warn members!")
        return
    
    try:
        embed = discord.Embed(
            title="⚠️ Warning",
            description=f"{member.mention} has been warned!",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        embed.add_field(name="Warned by", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
        
        try:
            await member.send(f"⚠️ You have been warned in {ctx.guild.name}. Reason: {reason or 'No reason provided'}")
        except discord.Forbidden:
            await ctx.send("⚠️ Warning issued, but I couldn't DM the user.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def clear(ctx, amount: int):
    """Deletes a specified number of messages."""
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ You don't have permission to manage messages!")
        return
    
    if amount < 1 or amount > 100:
        await ctx.send("❌ Please specify a number between 1 and 100!")
        return
    
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"✅ Deleted {len(deleted) - 1} messages!")
        await msg.delete(delay=3)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    """Mutes a member indefinitely (timeout for 28 days)."""
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ You don't have permission to mute members!")
        return
    
    try:
        from datetime import timedelta
        await member.timeout(timedelta(days=28), reason=reason)
        await ctx.send(f"🔇 {member.mention} has been muted. Reason: {reason or 'No reason provided'}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to mute this member!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def unmute(ctx, member: discord.Member):
    """Unmutes a member."""
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.send("❌ You don't have permission to unmute members!")
        return
    
    try:
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} has been unmuted!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to unmute this member!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def slowmode(ctx, seconds: int):
    """Sets slowmode for the current channel."""
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ You don't have permission to manage channels!")
        return
    
    if seconds < 0 or seconds > 21600:
        await ctx.send("❌ Slowmode must be between 0 and 21600 seconds (6 hours)!")
        return
    
    try:
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send("✅ Slowmode disabled!")
        else:
            await ctx.send(f"✅ Slowmode set to {seconds} seconds!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to edit this channel!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def lock(ctx):
    """Locks the current channel."""
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ You don't have permission to manage channels!")
        return
    
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Channel locked!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to edit this channel!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def unlock(ctx):
    """Unlocks the current channel."""
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ You don't have permission to manage channels!")
        return
    
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
        await ctx.send("🔓 Channel unlocked!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to edit this channel!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def userinfo(ctx, member: Optional[discord.Member] = None):
    """Shows information about a user."""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"User Info - {member}",
        color=member.color
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown", inline=True)
    embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles[1:]]) or "None", inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    """Shows information about the server."""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.blue()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: Optional[discord.Member] = None):
    """Shows a user's avatar."""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"{member.name}'s Avatar",
        color=discord.Color.blue()
    )
    embed.set_image(url=member.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    """Shows the bot's latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: {latency}ms")

@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    """Adds a role to a member."""
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ You don't have permission to manage roles!")
        return
    
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ Added {role.mention} to {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to add this role!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    """Removes a role from a member."""
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ You don't have permission to manage roles!")
        return
    
    try:
        await member.remove_roles(role)
        await ctx.send(f"✅ Removed {role.mention} from {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to remove this role!")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {str(e)}")

@bot.command()
async def poll(ctx, question: str, *options):
    """Creates a poll with reactions. Usage: n/poll "question" option1 option2 ..."""
    if len(options) < 2:
        await ctx.send("❌ Please provide at least 2 options!")
        return
    
    if len(options) > 10:
        await ctx.send("❌ Maximum 10 options allowed!")
        return
    
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    
    description = "\n".join([f"{reactions[i]} {option}" for i, option in enumerate(options)])
    
    embed = discord.Embed(
        title=f"📊 {question}",
        description=description,
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Poll by {ctx.author}")
    
    poll_message = await ctx.send(embed=embed)
    
    for i in range(len(options)):
        await poll_message.add_reaction(reactions[i])

@bot.command()
async def announce(ctx, *, message: str):
    """Sends a formatted announcement."""
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ You don't have permission to make announcements!")
        return
    
    embed = discord.Embed(
        title="📢 Announcement",
        description=message,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Announced by {ctx.author}")
    
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass
    await ctx.send(embed=embed)

# Get token from environment variable
token = os.getenv("BOT_TOKEN") or os.getenv("DISCORD_BOT_TOKEN")
if not token:
    print("❌ Error: BOT_TOKEN or DISCORD_BOT_TOKEN environment variable is not set.")
    print("Please add your Discord bot token to the Secrets.")
    exit(1)


import os
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
print("Token is:", TOKEN)  # for debugging
bot.run(TOKEN)
