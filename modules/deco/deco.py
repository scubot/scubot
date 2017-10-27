from modules.botModule import BotModule


class Deco(BotModule):
    name = 'deco'  # name of your module

    description = 'This module preforms decompression calculations using the Buehlmann ZH-16 decompression algorithm with gradient factors'  # description of its function

    help_text = ''  # help text for explaining how to do things

    trigger_string = '!deco'  # string to listen for as trigger

    has_background_loop = False  # start background loop

    module_version = '0.0.1'  # version of the current module

    def __init__(self):
        BotModule.__init__(self)

    async def parse_command(self, message, client):
        await client.send_message(message.channel, 'deco works')
