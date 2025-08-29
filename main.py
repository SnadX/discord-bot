# main.py
# imports
import asyncio
from collections import deque
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import random
import requests
from yt_dlp import YoutubeDL

# env, logging and intents setup
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='?', intents=intents)

# Options for yt-dlp downloader
ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'postprocessors':
    [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

# Options for ffmpeg
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ydl = YoutubeDL(ydl_opts)

song_queue = deque()

# Searches for song
async def search_yt(query):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))

    # Takes first item from playlist
    if "entries" in data:
        data = data["entries"][0]

    song_queue.append({'title': data["title"], 'url': data["url"]})

# Event Listeners
@bot.event
async def on_ready():
    print(f"{bot.user.name} has logged in")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # TODO Implement some kind of automod
    await bot.process_commands(message)

# Role reacts
# Adds a role to the user depending on the reaction to the message
# Can additionally check payload.message_id or payload.channel_id to ensure it only works in a specific message/channel
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    user = discord.utils.get(guild.members, id=payload.user_id)
    if user.bot: return
    # if payload.message_id != <Message ID here>: return
    match str(payload.emoji):
        case "1️⃣":
            role =  discord.utils.get(guild.roles, name="Test Role 1")
        case "2️⃣":
            role =  discord.utils.get(guild.roles, name="Test Role 2")
        case "3️⃣":
            role =  discord.utils.get(guild.roles, name="Test Role 3")
        case _:
            return

    await user.add_roles(role)
    print(f"Added role '{role.name}' to user '{user.name}'")

# Removes a role from the user depending on the reaction to the message
@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    user = discord.utils.get(guild.members, id=payload.user_id)
    if user.bot: return
    # if payload.message_id != <Message ID here>: return
    match str(payload.emoji):
        case "1️⃣":
            role =  discord.utils.get(guild.roles, name="Test Role 1")
        case "2️⃣":
            role =  discord.utils.get(guild.roles, name="Test Role 2")
        case "3️⃣":
            role =  discord.utils.get(guild.roles, name="Test Role 3")
        case _:
            return

    await user.remove_roles(role)
    print(f"Removed role '{role.name}' from user '{user.name}'")

# Commands
# bot.remove_command('help')
'''
@bot.command()
async def help(ctx):
    # TODO send a message containing a formatted list of all bot commands
    return
'''

# Repeats author's message
@bot.command()
async def echo(ctx, *, args):
    await ctx.send(args)

# Purges N most recent messages 
# TODO add a check for admin permissions - admin role in ctx.message.author.roles
@bot.command()
async def clear(ctx, num: int=10):
    try:
        await ctx.message.delete()
        deleted =  await ctx.message.channel.purge(limit=num)
        await ctx.send(f"Deleted {len(deleted)} message(s)")
    except:
        await ctx.reply("Usage: ?clear <number of messages to delete>")

# Creates an embed that assigns users roles when they react
@bot.command()
async def roleassigner(ctx):
    embed = discord.Embed(title="React to assign roles")
    embed.description = ("1️⃣ Test Role 1\n 2️⃣ Test Role 2\n 3️⃣ Test Role 3")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")

# Sends the user a reminder
@bot.command()
async def remindme(ctx, num: int, time: str, *, msg: str=""):
    try:
        reminder = discord.utils.utcnow()
        match time:
            case 'minute' | 'minutes':
                reminder = reminder + datetime.timedelta(minutes=num)
            case 'hour' | 'hours':
                reminder = reminder + datetime.timedelta(hours=num)
            case 'day' | 'days':
                reminder = reminder + datetime.timedelta(days=num)

        title = msg if msg else "A reminder has been set for"
        await ctx.message.author.send(f"{title}\n{discord.utils.format_dt(reminder)}")

    except:
        await ctx.send('Usage: ?remindme <number> <minute(s)|hour(s)|day(s)> <[optional] message>')

# Rolls NdN dice
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, sides = map(int, dice.lower().split('d'))
        await ctx.send(f"You rolled: {' '.join([str(random.randint(1, sides)) for i in range(rolls)])}")
    except:
        await ctx.reply("Usage: ?roll NdN")

# Cool fact
@bot.command()
async def fact(ctx, arg: str=""):
    choice = ""
    match arg:
        case "":
            choice = "today"
        case "random":
            choice = "random"
        case _:
            await ctx.reply("Usage: ?fact or ?fact random")
            return

    r = requests.get(f"https://uselessfacts.jsph.pl/api/v2/facts/{choice}")
    await ctx.send(r.json()['text'])

# Music Commands
# Connect to voice channel and play music
@bot.command()
async def play(ctx, *, args):
    # Check if the user is in a voice channel
    if ctx.message.author.voice is None:
        await ctx.reply("You must be in a voice channel to do this")
        return

    vc = ctx.message.author.voice.channel

    # Join the voice channel
    if ctx.voice_client:
        await ctx.voice_client.move_to(vc)
    else:
        await vc.connect()

    # Search and play audio
    query = "ytsearch1:" + args
    await search_yt(query)
    if not (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
        play_next_song(ctx)
    else:
        await ctx.send(f"Added {song_queue[-1]['title']} to queue in position {len(song_queue)}")

# Plays next song in queue
def play_next_song(ctx):
    if not song_queue:
        return

    song = song_queue.popleft()
    title = song['title']
    url = song['url']

    source = discord.FFmpegOpusAudio(url, **ffmpeg_options)
    ctx.voice_client.play(source, after=lambda e: play_next_song(ctx))
    asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: {title}"), bot.loop) 
    
# Pauses audio
@bot.command()
async def pause(ctx):
    ctx.voice_client.pause()

# Unpauses audio
@bot.command()
async def unpause(ctx):
    ctx.voice_client.resume()

# Skips current track
@bot.command()
async def skip(ctx):
    ctx.voice_client.stop()

# Displays music queue
@bot.command()
async def queue(ctx):
    if not song_queue:
        await ctx.send("The song queue is empty.")
    else:
        msg = [f"{song_queue.index(song) + 1}. {song['title']}" for song in song_queue]
        await ctx.send('\n'.join(msg))

# Leaves the voice channel
@bot.command()
async def leave(ctx):
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()

# Runs the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)