from discord.ext import commands
import discord

class Role(commands.Cog):
    def __init__(self, bot):
        self.version = "2.0.1"
        self.bot = bot

    @commands.command()
    async def role(self, ctx, *, role: discord.Role = None):
        """
        Add yourself the specified role group.
        """
        if role is None:
            return await ctx.send("[!] You did not specify a role.")
        try:
            await ctx.author.add_roles(role)
            await ctx.send(f"[:ok_hand:] Assigned you to {role.name}.")
        except discord.Forbidden:
            await ctx.send("[!] Could not assign you to that role.")

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
