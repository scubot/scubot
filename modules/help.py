import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        emb = discord.Embed(
            title="Scubot Help",
            description=f"Use `{self.clean_prefix}help [command]` for more info on a command.",
            colour=0x008080
        )
        command_mapping = {}
        for cog in self.context.bot.cogs.values():
            cog_commands = await self.filter_commands(cog.get_commands(), sort=True)
            if cog_commands:
                command_mapping[cog.qualified_name] = [c.name for c in cog_commands]

        available_command_str = "\n".join(
            [f"{name}: {', '.join(commands)}" for name, commands in command_mapping.items()]
        )
        emb.add_field(name="Available Commands", value=available_command_str)
        await self.context.send(embed=emb)

    async def send_command_help(self, command):
        emb = discord.Embed(title="Scubot Help", description=f"```{self.get_command_signature(command)}```",
                            colour=0x008080)
        emb.add_field(name="Details", value=command.help or "No details available.", inline=False)
        emb.add_field(name="Aliases",
                      value=f"```{', '.join(command.aliases)}```" if command.aliases else "No aliases exist.",
                      inline=False)
        await self.context.send(embed=emb)

    async def send_group_help(self, group):
        emb = discord.Embed(title="Scubot Help",
                            description=f"Help for `{group.name}` command group.\nUse `{self.clean_prefix}help {group.name} [command]` for more info on a command.",
                            colour=0x008080)
        emb.add_field(name="Details", value=group.help or "No details available.", inline=False)
        emb.add_field(name="Available Subcommands",
                      value=f"```\n{', '.join([command.name for command in group.commands])}\n```", inline=False)
        await self.context.send(embed=emb)

    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self
        self.version = "1.0.0"

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
