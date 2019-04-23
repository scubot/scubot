import time
from discord.ext import commands
import discord
import json


class Status(commands.Cog):
    def __init__(self, bot):
        self.version = "2.0.0"
        self.bot = bot
        self.start_time = time.time()

    @staticmethod
    def get_bot_version(file):
        if file:
            with open(file, 'r') as f:
                return json.load(f)

    @staticmethod
    def uptime_convert(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    @staticmethod
    def loaded_modules(bot):
        load = ''
        for key,value in bot.cogs.items():
            load += key + "(" + value.version + ")" + ", "
        return load[:-2]

    @commands.command()
    async def status(self, ctx):
        uptime = time.time() - self.start_time
        uptime_string = [str(round(x, 0))[:-2] for x in self.uptime_convert(uptime)]
        uptime_string = uptime_string[0] + 'd ' + uptime_string[1] + 'h ' + uptime_string[2] + 'm ' + uptime_string[
            3] + 's'
        module_string = self.loaded_modules(self.bot)
        embed = discord.Embed(title="Status", description="Status and information about this bot", color=0x008080)
        embed.add_field(name="Uptime", value=uptime_string, inline=True)
        embed.add_field(name="Loaded Modules", value=module_string, inline=True)
        js = self.get_bot_version("config.json")
        embed.add_field(name="Bot version", value=js["version"], inline=True)
        embed.add_field(name="Donate", value=js["donation_link"], inline=True)
        embed.set_footer(text="Powered by scubot: https://github.com/scubot/scubot")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
