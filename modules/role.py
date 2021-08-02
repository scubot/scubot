from discord.ext import commands
import discord

class Role(commands.Cog):
    def __init__(self, bot):
        self.version = "2.0.1"
        self.bot = bot

    @commands.command()
    async def role(self, ctx):
        """
        Add yourself the specified role group.
        """
        role = ctx.message.content[5:].strip().split(" ")[-1].lower()
        if role == "":
            return await ctx.send("[!] You did not specify a role.")
        try:
            roles = ctx.guild.roles
            x = {}
            for i in roles:
                x[i.name.lower()] = i
            if role in x:
                await ctx.author.add_roles(x[role])
                await ctx.send(f"[:ok_hand:] Assigned you to {role}.")
            else:
                return await ctx.send("[!] Role does not exist!")
        except discord.Forbidden:
            await ctx.send("[!] Could not assign you to that role.")

    @commands.command()
    async def derole(self, ctx):
        """
        Remove yourself from the specified role group.
        """
        role = ctx.message.content[5:].strip().split(" ")[-1].lower()
        if role == "":
            return await ctx.send("[!] You did not specify a role.")
        try:
            roles = ctx.guild.roles
            x = {}
            for i in roles:
                x[i.name.lower()] = i
            if role in x:
                await ctx.author.remove_roles(x[role])
                await ctx.send(f"[:ok_hand:] Removed you from {role}.")
            else:
                return await ctx.send("[!] Role does not exist!")
        except discord.Forbidden:
            await ctx.send("[!] Could not remove you from that role.")


def setup(bot):
    bot.add_cog(Role(bot))
