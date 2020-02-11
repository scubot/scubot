import time

from discord.ext import commands
import discord
from discord.utils import find
from tinydb import *

class Role(commands.Cog):
    def __init__(self, bot):
        self.version = "2.0.1"
        self.bot = bot

    @commands.command()
    async def role(self, ctx, *, role: discord.Role = None):
        if role is None:
            return await ctx.send("[!] You did not specify a role.")
        try:
            await ctx.author.add_roles(role)
            await ctx.send(f"[:ok_hand:] Assigned you to {role.name}.")
        except discord.Forbidden:
            await ctx.send("[!] Could not assign you to that role.")

    @commands.command()
    async def role(self, ctx, *, role: str = None):
        if type(ctx.message.channel) != discord.TextChannel: # Check we are in a DM
            # First work out which guilds are valid, ie the user is in them and it has the role we are looking for
            guilds = [guild for guild in ctx.bot.guilds if
                      ctx.message.author.id in [member.id for member in guild.members] and role in [role.name for role
                                                                                                    in guild.roles]]
            if len(guilds) > 1:
                await ctx.send("[!] Multiple servers with same role, please run command again from preferred server")
            else:
                guild = guilds[0]
                user = find(lambda u: u.id == ctx.author.id, guild.members)
                role_to_assign = find(lambda r: r.name == role, guild.roles)
                try:
                    await user.add_roles(role_to_assign)
                    await ctx.send("[:ok_hand:] Assigned you to " + str(role_to_assign) + " .")
                except discord.Forbidden:
                    await ctx.send("[!] Could not assign you to that role.")
        else:
            await ctx.send(F"[!] Invalid argument: Role \"{role}\" not found.")

    @commands.command()
    async def derole(self, ctx, *, role: discord.Role = None):
        """
        Remove yourself from the specified role group.
        """
        if role is None:
            return await ctx.send("[!] You did not specify a role.")
        try:
            await ctx.author.remove_roles(role)
            await ctx.send(f"[:ok_hand:] Removed you from {role.name}.")
        except discord.Forbidden:
            await ctx.send("[!] Could not remove you from that role.")


def setup(bot):
    bot.add_cog(Role(bot))
