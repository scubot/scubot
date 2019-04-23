from discord.ext import commands


class Loader(commands.Cog):
    def __init__(self, bot):
        self.version = "1.0.0"
        self.bot = bot

    @commands.has_any_role('moderator', 'admin', 'devs')
    @commands.command()
    async def reload(self, ctx, *, module: str):
        print("[LOAD] Reloading " + module)
        self.bot.reload_extension(module)
        await ctx.send("[:ok_hand:] Module " + module + " was reloaded.")

    @commands.has_any_role('moderator', 'admin', 'devs')
    @commands.command()
    async def load(self, ctx, *, module: str):
        print("[LOAD] Loading " + module)
        self.bot.load_extension(module)
        await ctx.send("[:ok_hand:] Module " + module + " was loaded.")

    @commands.has_any_role('moderator', 'admin', 'devs')
    @commands.command()
    async def unload(self, ctx, *, module: str):
        print("[LOAD] Unloading " + module)
        self.bot.unload_extension(module)
        await ctx.send("[:ok_hand:] Module " + module + " was unloaded.")

    @reload.error
    @load.error
    @unload.error
    async def loading_error_handler(self, ctx, error):
        print("[WARN] " + str(error.original))
        if isinstance(error.original, commands.ExtensionNotLoaded):
            await ctx.send("[!] Module not already loaded.")
            return
        if isinstance(error.original, commands.ExtensionAlreadyLoaded):
            await ctx.send("[!] Module already loaded.")
            return
        if isinstance(error.original, commands.ExtensionNotFound):
            await ctx.send("[!] Module not found!")
            return
        if isinstance(error.original, commands.NoEntryPointError):
            await ctx.send("[!] Module has no entry point!")
            return
        if isinstance(error.original, commands.ExtensionFailed):
            await ctx.send("[!] Module setup encountered execution error! Check logs for details.")
            return


def setup(bot):
    bot.add_cog(Loader(bot))
