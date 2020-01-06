from discord.ext import commands

from modules.dispatch import EmbedChain
from util.missingdependency import MissingDependencyException


class DispatchExample(commands.Cog):
    def __init__(self, bot):
        self.version = "0.1.0"
        self.bot = bot
        self.dispatcher = bot.get_cog("Dispatcher")

    @staticmethod
    def create_embedchain(pages: int) -> EmbedChain:
        return EmbedChain([["Hello", x] for x in range(1, pages+1)], limit=1, color=0x64c891, title="Dispatch Example",
                          inline=True)

    @commands.group(invoke_without_command=True)
    async def dispatch_example(self, ctx, pages: int = 5):
        embed = self.create_embedchain(pages)
        sent_message = await ctx.send(embed=embed.current())
        await self.dispatcher.register(sent_message, embed)


def setup(bot):
    if not bot.get_cog("Dispatcher"):
        raise MissingDependencyException("Dispatcher")
    bot.add_cog(DispatchExample(bot))
