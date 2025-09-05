# main.py
# imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import os

# env, logging and intents setup
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='?', intents=intents)

# Modified help command
class MyHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            await destination.send(embed=embed)

bot.help_command = MyHelp()

# Loads cogs from cogs directory
async def load_cogs():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f"cogs.{file[:-3]}")

# Event Listeners
@bot.event
async def on_ready():
    await load_cogs()
    print(f"{bot.user.name} has logged in")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

# Runs the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)