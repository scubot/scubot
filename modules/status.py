import discord
from modules.botModule import BotModule
from modules.help import *
import time
import datetime


class Status(BotModule):
    name = 'status'

    description = 'Shows status about this bot.'

    help_text = 'Usage: `!status` shows information about this instance of scubot.'

    trigger_string = 'status'

    init_time = time.time()

    bot_version = ''

    module_version = '1.0.0'

    def __init__(self, bot_version):
        BotModule.__init__(self)
        self.bot_version = bot_version

    def uptime_convert(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds

    async def parse_command(self, message, discord_interface):
        if message.channel.id in self.admin_modules:
            uptime = time.time() - self.init_time
            uptime_string = [str(round(x, 0))[:-2] for x in self.uptime_convert(uptime)]
            uptime_string = uptime_string[0] + 'd ' + uptime_string[1] + 'h ' + uptime_string[2] + 'm ' + uptime_string[
                3] + 's'
            module_string = ''
            for botModule in self.loaded_modules:
                module_string += botModule.name + ' (' + botModule.module_version + '), '
            module_string = module_string[:-2]
            msg = '```\n Uptime: ' + uptime_string + '\n' \
                  'Loaded modules: ' + module_string + '\n' \
                  'Bot version: ' + self.bot_version + '\n' \
                  'Powered by scubot: https://github.com/scubot/scubot```'
            await discord_interface.send_message(message.channel, msg)
        else:
            return
