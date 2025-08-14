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

# Rolls NdN dice
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, sides = map(int, dice.lower().split('d'))
        await ctx.send(f"You rolled: {' '.join([str(random.randint(1, sides)) for i in range(rolls)])}")
    except:
        await ctx.send("Usage: ?roll NdN")

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