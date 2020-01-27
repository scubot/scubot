from discord.ext import commands


class Loader(commands.Cog):
    def __init__(self, bot):
        self.version = "1.0.1"
        self.bot = bot

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def reload(self, ctx, *, module: str):
        print(f"[LOAD] Reloading {module}")
        self.bot.reload_extension(module)
        await ctx.send(f"[:ok_hand:] Module {module} was reloaded.")

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def load(self, ctx, *, module: str):
        print(f"[LOAD] Loading {module}")
        self.bot.load_extension(module)
        await ctx.send(f"[:ok_hand:] Module {module} was loaded.")

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def unload(self, ctx, *, module: str):
        print(f"[LOAD] Unloading {module}")
        self.bot.unload_extension(module)
        await ctx.send(f"[:ok_hand:] Module {module} was unloaded.")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            print(f"[WARN] {str(error)}")
        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send("[!] Module not already loaded.")
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send("[!] Module already loaded.")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send("[!] Module not found!")
        elif isinstance(error, commands.NoEntryPointError):
            await ctx.send("[!] Module has no entry point!")
        elif isinstance(error, commands.ExtensionFailed):
            await ctx.send("[!] Module setup encountered execution error! Check logs for details.")


def setup(bot):
    bot.add_cog(Loader(bot))
