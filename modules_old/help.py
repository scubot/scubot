import discord
from modules_old.botModule import BotModule
import shlex


class Help(BotModule):
    name = 'help'  # name of your module

    description = 'This provides help for other '  # description of its function

    help_text = "Write !help followed by the name of the module to access it's help text, for example !help Units " \
                ' will access the help for the Units module. Type !help Modules to see loaded modules_old.'  # help text for explaining how to do things

    trigger_string = 'help'  # string to listen for as trigger

    module_version = '1.0.0'

    direct_mode = True  # Send messages via DM instead of in the channel

    async def parse_command(self, message, client):
        msg = shlex.split(message.content)
        if len(msg) == 1:
            await self.send_message(client, message, "Help: \n\n" + self.help_text)
        else:
            module_name = msg[1].lower()
            if module_name == 'modules_old':
                module_string = ''
                for botModule in self.loaded_modules:
                    module_string += botModule.name + ', '
                module_string = module_string[:-2]
                await self.send_message(client, message, 'Loaded modules_old: \n\n' + module_string)
            for botModule in self.loaded_modules:
                if botModule.name == module_name:
                    if botModule.help_text == '':
                        await self.send_message(client, message, botModule.name + ' has no help text, tell the module '
                                                                                  'maintainer to fix it')
                    else:
                        await self.send_message(client, message, botModule.name + ": \n\n " + botModule.help_text)

    async def send_message(self, client, message, send):
        if self.direct_mode:
            await client.send_message(message.author, send)
        else:
            await client.send_message(message.channel, send)
