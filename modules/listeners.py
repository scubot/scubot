import discord
from discord.ext import commands
import traceback
import sys


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version = "1.0.0"
        self.visible = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("\n-------------------")
        print("Bot logged in successfully:")
        print(f"User: {str(self.bot.user)}")
        print(f"ID: {self.bot.user.id}")
        print("-------------------")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):  # Command not found, not our fault.
            return
        if isinstance(error,
                      discord.ext.commands.MissingRequiredArgument):  # Missing some sort of argument - who knows?
            return await ctx.send("[!] Missing required argument.")
        if isinstance(error, discord.ext.commands.CheckFailure):
            return await ctx.send(f"[!] I'm sorry {ctx.author.name}, I'm afraid I can't do that.")
        if isinstance(error, discord.ext.commands.ExtensionError):
            return  # Already handled in loader
        if isinstance(error, discord.ext.commands.errors.BadArgument):
            return await ctx.send(f"[!] Invalid argument: {error.args[0]}")

        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(Listeners(bot))
