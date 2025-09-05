# misc.py
# imports
import datetime
import discord
from discord.ext import commands
import random
import requests

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, args: str):
        """Repeats the user's message"""
        await ctx.send(args)

    @commands.command()
    async def clear(self, ctx, num: int=10):
        """Deletes a number of the most recent messages specified by the user"""
        try:
            await ctx.message.delete()
            deleted =  await ctx.channel.purge(limit=num)
            await ctx.send(f"Deleted {len(deleted)} message(s)")
        except:
            await ctx.reply("Usage: ?clear <number of messages to delete>")

    @commands.command()
    async def remindme(self, ctx, num: int, time: str, *, msg: str=""):
        """DMs the user a reminder set after the specified amount of time"""
        try:
            reminder = discord.utils.utcnow()
            match time:
                case 'minute' | 'minutes':
                    reminder = reminder + datetime.timedelta(minutes=num)
                case 'hour' | 'hours':
                    reminder = reminder + datetime.timedelta(hours=num)
                case 'day' | 'days':
                    reminder = reminder + datetime.timedelta(days=num)

            title = msg if msg else "Reminder"
            embed = discord.Embed(title=title)
            embed.description = discord.utils.format_dt(reminder)
            await ctx.author.send(embed=embed)

        except:
            await ctx.send('Usage: ?remindme <number> <minute(s)|hour(s)|day(s)> <[optional] message>')

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls dice given in the format NdN"""
        try:
            rolls, sides = map(int, dice.lower().split('d'))
            embed = discord.Embed(title="Results")
            embed.description = f"{', '.join([str(random.randint(1, sides)) for i in range(rolls)])}"
            await ctx.send(embed=embed)
        except:
            await ctx.reply("Usage: ?roll NdN")

    @commands.command()
    async def fact(self, ctx, arg: str=""):
        """This is a cool fact"""
        choice = ""
        title = ""
        match arg:
            case "":
                choice = "today"
                title = "Fact of the day"
            case "random":
                choice = "random"
                title = "Random Fact"
            case _:
                await ctx.reply("Usage: ?fact or ?fact random")
                return

        r = requests.get(f"https://uselessfacts.jsph.pl/api/v2/facts/{choice}")
        embed = discord.Embed(title=title)
        embed.description = r.json()['text']
        await ctx.send(embed=embed)

async def setup(bot):
    print("Loading misc")
    await bot.add_cog(Misc(bot))