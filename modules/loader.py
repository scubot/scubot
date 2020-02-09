from discord.ext import commands


class Loader(commands.Cog):
    def __init__(self, bot):
        self.version = "1.0.1"
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            print(f"[WARN] {str(error)}")
            if isinstance(error.original, commands.errors.ExtensionNotLoaded):
                return await ctx.send("[!] Module not already loaded.")
            elif isinstance(error.original, commands.errors.ExtensionAlreadyLoaded):
                return await ctx.send("[!] Module already loaded.")
            elif isinstance(error.original, commands.errors.ExtensionNotFound):
                return await ctx.send("[!] Module not found!")
            elif isinstance(error.original, commands.errors.NoEntryPointError):
                return await ctx.send("[!] Module has no entry point!")
            elif isinstance(error.original, commands.errors.ExtensionFailed):
                return await ctx.send("[!] Module setup encountered execution error! Check logs for details.")

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def reload(self, ctx, *, module: str):
        """
        Reload the specified bot module.
        """
        print(f"[LOAD] Reloading {module}")
        self.bot.reload_extension(module)
        await ctx.send(f"[:ok_hand:] Module {module} was reloaded.")

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def load(self, ctx, *, module: str):
        """
        Load the specified bot module.
        """
        print(f"[LOAD] Loading {module}")
        self.bot.load_extension(module)
        await ctx.send(f"[:ok_hand:] Module {module} was loaded.")

    @commands.has_any_role('Moderators', 'Admin', 'devs')
    @commands.command()
    async def unload(self, ctx, *, module: str):
        """
        Unload the specified bot module.
        """
        print(f"[LOAD] Unloading {module}")
        self.bot.unload_extension(module)
        await ctx.send(f"[:ok_hand:] Module {module} was unloaded.")


def setup(bot):
    bot.add_cog(Loader(bot))
