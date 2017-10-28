import discord
from modules.botModule import BotModule
import shlex


class Info(BotModule):
    name = 'info'  # name of your module

    description = 'This provides descriptions about module features.'  # description of its function

    help_text = "Write !info followed by the name of the module to access it's description, for example !info Units " \
                ' will access the description of the Units module.'  # help text for explaining how to do things

    trigger_string = '!info'  # string to listen for as trigger

    module_version = '1.0.0'

    async def parse_command(self, message, client):
        msg = shlex.split(message.content)
        if len(msg) == 1:
            await client.send_message(message.channel, self.help_text)
        else:
            module_name = msg[1].lower()
            for botModule in self.loaded_modules:
                if botModule.name == module_name:
                    if botModule.description == '':
                        await client.send_message(message.channel,
                                                  botModule.name + ' has no description, tell the module '
                                                                   'maintainer to fix it')
                    else:
                        await client.send_message(message.channel, botModule.description)
