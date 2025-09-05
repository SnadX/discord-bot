# role_reacts.py
# imports
import discord
from discord.ext import commands

class RoleReacts(commands.Cog, name="Role Reacts"):
    def __init__(self, bot):
        self.bot = bot

    # Adds a role to the user depending on the reaction to the message
    # Can additionally check payload.message_id or payload.channel_id to ensure it only works in a specific message/channel
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # if payload.message_id != <Message ID here>: return
        guild = self.bot.get_guild(payload.guild_id)
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

    # Removes a role from the user depending on the reaction to the message
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # if payload.message_id != <Message ID here>: return
        guild = self.bot.get_guild(payload.guild_id)
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

    @commands.command()
    async def roleassigner(self, ctx):
        """Creates an embed that assigns users roles when they use specific reactions"""
        embed = discord.Embed(title="React to assign roles")
        embed.description = ("1️⃣ Test Role 1\n 2️⃣ Test Role 2\n 3️⃣ Test Role 3")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")

async def setup(bot):
    print("Loading role reacts")
    await bot.add_cog(RoleReacts(bot))