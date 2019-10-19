import json
import time
import uuid

import discord
from discord.ext import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.version = "2.1.0"
        self.bot = bot
        self.start_time = time.time()

    @staticmethod
    def uptime_convert(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    def loaded_modules(self):
        load = ''
        for key, value in self.bot.cogs.items():
            try:
                uuid.UUID(key)
                continue
            except ValueError:
                load += key + " (" + value.version + ")" + ", "
        return load[:-2]

    def get_latency(self):
        return "{:0.2f}ms".format((self.bot.latency * 1000))

    @commands.command()
    async def status(self, ctx):
        uptime = time.time() - self.start_time
        uptime_string = [str(round(x, 0))[:-2] for x in self.uptime_convert(uptime)]
        uptime_string = uptime_string[0] + 'd ' + uptime_string[1] + 'h ' + uptime_string[2] + 'm ' + uptime_string[
            3] + 's'
        module_string = self.loaded_modules()
        embed = discord.Embed(title="Status", description="Status and information about this bot", color=0x008080)
        embed.add_field(name="Uptime", value=uptime_string, inline=False)
        embed.add_field(name="Loaded Modules", value=module_string, inline=False)
        embed.add_field(name="Bot version", value=self.bot.version, inline=False)
        embed.add_field(name="Latency", value=self.get_latency(), inline=False)
        embed.add_field(name="Donate", value="https://www.paypal.me/theansoncheung", inline=False)
        embed.set_footer(text="Powered by scubot: https://github.com/scubot/scubot")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
