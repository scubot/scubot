import discord
from modules.botModule import BotModule
import shlex


class Help(BotModule):
    name = 'Help'  # name of your module

    description = 'This provides help for other '  # description of its function

    help_text = "Write !help followed by the name of the module to access it's help text, for example !help Units " \
                ' will access the help for the Units module.'  # help text for explaining how to do things

    trigger_string = '!help'  # string to listen for as trigger

    loaded_modules = []

    def __init__(self, loaded_modules):
        self.loaded_modules = loaded_modules

    async def parse_command(self, message, client):
        msg = shlex.split(message.content)
        module_name = msg[1]
        for botModule in self.loaded_modules:
            if botModule.name == module_name:
                if botModule.help_text == '':
                    await client.send_message(message.channel, botModule.name + ' has no help text, tell the module '
                                                                                'maintainer to fix it')
                else:
                    await client.send_message(message.channel, botModule.help_text)
