# main.py
# imports
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os
import random
import requests

# env, logging and intents setup
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='?', intents=intents)

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
# Can additionally check payload.message_id or payload.channel_id to ensure it only works in a specific message/channel
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    user = discord.utils.get(guild.members, id=payload.user_id)
    if user.bot: return
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

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    user = discord.utils.get(guild.members, id=payload.user_id)
    if user.bot: return
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
        await ctx.send("Usage: ?clear <number of messages to delete>")

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
        await ctx.send("Usage: ?roll NdN")

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
            await ctx.send("Usage: ?fact or ?fact random")
            return
    
    r = requests.get(f"https://uselessfacts.jsph.pl/api/v2/facts/{choice}")
    await ctx.send(r.json()['text'])

# Music Commands
@bot.command()
async def play(ctx, *, args):
    # TODO Implement
    return

@bot.command()
async def pause(ctx, *, args):
    # TODO Implement
    return

@bot.command()
async def skip(ctx, *, args):
    # TODO Implement
    return

@bot.command()
async def queue(ctx, *, args):
    # TODO Implement
    return

# Runs the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)