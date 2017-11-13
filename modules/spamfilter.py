import discord
import shlex
from modules.botModule import BotModule

class SpamFilter():
    name = 'spamfilter'  # name of your module

    description = 'Detects and prevents spam behaviour.'  # description of its function

    help_text = 'This module has no callable functions.'  # help text for explaining how to do things

    trigger_string = ''  # string to listen for as trigger

    has_background_loop = False

    listen_for_reaction = False

    module_version = '0.1.0'

    async def on_message(self, message, client):
        # TODO: Rules would be implemented here
        pass
