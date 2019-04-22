import time

from discord.ext import commands
import discord
from discord.utils import find
from tinydb import *

class Role(commands.Cog):
    def __init__(self, bot):
        self.version = "2.0.0"
        self.bot = bot

    @commands.command()
    async def role(self, ctx, *, role: str = None):
        role_to_assign = find(lambda r: r.name == role, ctx.message.guild.roles)
        try:
            await ctx.author.add_roles(role_to_assign)
            await ctx.send("[:ok_hand:] Assigned you to " + str(role_to_assign) + " .")
        except discord.Forbidden:
            await ctx.send("[!] Could not assign you to that role.")

    @commands.command()
    async def derole(self, ctx, *, role: str = None):
        role_to_remove = find(lambda r: r.name == role, ctx.message.guild.roles)
        try:
            await ctx.author.remove_roles(role_to_remove)
            await ctx.send("[:ok_hand:] Removed you from " + str(role_to_remove) + " .")
        except discord.Forbidden:
            await ctx.send("[!] Could not remove you from that role.")


def setup(bot):
    bot.add_cog(Role(bot))
