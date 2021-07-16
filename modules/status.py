import datetime

import discord
from discord.ext import commands

DEFAULT_VERSION = "(?.?.?)"


class Status(commands.Cog):
    def __init__(self, bot):
        self.version = "2.1.1"
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

    @staticmethod
    def uptime_convert(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    def loaded_modules(self):
        output = []
        for name, cog in self.bot.cogs.items():
            if hasattr(cog, "visible"):
                if not cog.visible:
                    continue

            if hasattr(cog, "version"):
                output.append(f"{name} ({cog.version})")
            else:
                output.append(f"{name} {DEFAULT_VERSION}")
        return ", ".join(output)

    def get_latency(self):
        return "{:0.2f}ms".format((self.bot.latency * 1000))

    @commands.command()
    async def status(self, ctx):
        """
        Show general information about scubot.
        """
        current_time = datetime.datetime.utcnow()
        d, h, m, s = self.uptime_convert((current_time - self.start_time).seconds)
        module_string = self.loaded_modules()
        embed = discord.Embed(title="Status", description="Status and information about this bot", color=0x008080)
        embed.add_field(name="Uptime", value=f"{d}d {h}h {m}m {s}s", inline=False)
        embed.add_field(name="Loaded Modules", value=module_string, inline=False)
        embed.add_field(name="Bot version", value=self.bot.version, inline=False)
        embed.add_field(name="Latency", value=self.get_latency(), inline=False)
        embed.add_field(name="Donate", value="https://www.paypal.me/theansoncheung", inline=False)
        embed.set_footer(text="Powered by scubot: https://github.com/scubot/scubot")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
