import discord
from discord.ext import commands

UNIT_PAIRS = {
    "psi": "br",
    "br": "psi",
    "ft": "m",
    "m": "ft",
    "lbs": "kg",
    "kg": "lbs",
    "fsw": "m",
}
SYMBOL_MAP = {
    "pounds per square inch": "psi",
    "bar": "br",
    "feet": "ft",
    "meters": "m",
    "pounds": "lbs",
    "kilograms": "kg",
    "fathoms": "fsw",
}
CONVERSION_RATES = {
    "psi": 0.068947697587212,
    "ft": 0.3048,
    "m": 3.28084,
    "lbs": 0.453592,
    "kg": 2.20462,
    "fsw": 1.8288,
    "br": 14.5038,
}


class Units(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version = "2.0.0"

    def convert_unit(self, amount, unit):
        if unit in SYMBOL_MAP.keys():
            unit = SYMBOL_MAP[unit]
        result = amount * CONVERSION_RATES[unit]
        return f"{amount} {unit} is equal to {result:.2f} {UNIT_PAIRS[unit]}."

    @commands.command()
    async def convert(self, ctx, amount=None, unit=None):
        """
		This module supports two types of conversion, explicit and implicit.
		Explicit conversion takes the form "!convert <number> <unit>" (e.g !convert 10 ft) and will post a conversion.
		Implicit conversion takes the form of "!convert" or "!convert all", "!convert" looks through the past 10 messages and converts the first unit it finds.
		Alternatively, by using "!convert all" it will convert all the units found in the past 10 messages.
		"""
        if amount is None and unit is None:
            channel_hist = await ctx.history(limit=10).flatten()
            for message in channel_hist:
                message_parts = message.content.split(maxsplit=1)
                if message_parts[0].isdigit():
                    if (
                        message_parts[1] in SYMBOL_MAP.keys()
                        or message_parts[1] in SYMBOL_MAP.values()
                    ):
                        converted_unit = self.convert_unit(
                            float(message_parts[0]), message_parts[1]
                        )
                        return await ctx.send(converted_unit)
            return await ctx.send(
                "[!] No valid conversions found in the last 10 messages."
            )

        elif amount == "all":
            output = []
            channel_hist = await ctx.history(limit=10).flatten()
            for message in channel_hist:
                message_parts = message.content.split(maxsplit=1)
                if message_parts[0].isdigit():
                    if (
                        message_parts[1] in SYMBOL_MAP.keys()
                        or message_parts[1] in SYMBOL_MAP.values()
                    ):
                        output.append(
                            self.convert_unit(float(message_parts[0]), message_parts[1])
                        )
            if not output:
                return await ctx.send(
                    "[!] No valid conversions found in the last 10 messages."
                )
            else:
                output = "\n".join(output)
                return await ctx.send(f"[:ok_hand:]\n{output}")
        else:
            if amount is None:
                return await ctx.send("[!] No amount provided.")
            elif unit is None:
                return await ctx.send("[!] No unit provided. ")
            else:
                try:
                    converted_unit = self.convert_unit(float(amount), unit)
                except KeyError:
                    try:
                        converted_unit = self.convert_unit(
                            float(amount), SYMBOL_MAP[unit]
                        )
                    except KeyError:
                        return await ctx.send(
                            "[!] The conversion you requested is invalid."
                        )
                return await ctx.send(f"[:ok_hand:] {converted_unit}")

    @commands.command()
    async def units(self, ctx):
        """
        Show a summary of all available units to be used with the convert command.
        """
        embed = discord.Embed(title="All available units:", colour=0x008080)
        embed.description = "\n".join((f"{k} = {v}" for k, v in SYMBOL_MAP.items()))
        embed.set_footer(text="Powered by scubot: https://github.com/scubot/scubot")
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Units(bot))
