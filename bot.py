import os
import discord

# Create a new Discord client (the "bot")
bot = discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "hello":
        await message.channel.send("Hi there! 👋")

# Run the bot using your token stored in Render's environment
bot.run(os.environ["DISCORD_TOKEN"])
