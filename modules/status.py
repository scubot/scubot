import discord
from modules.botModule import BotModule
from modules.help import *
import time
import datetime

class Status(BotModule):
        name = 'status'

        description = 'Allow for the assignment and removal of roles.'

        help_text = 'Usage: `!status` shows information about this instance of scubot.'

        trigger_string = '!status'

        init_time = 0

        def __init__(self):
            init_time = time.time()

        def uptime_convert(self,seconds):
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            return days, hours, minutes, seconds

        async def parse_command(self, message, client):
            uptime = self.init_time - time.time()
            uptime_string = self.uptime_convert(uptime)
            uptime_string = [str(round(x,0))[:-2] for x in uptime_string]
            uptime_string = uptime_string[0] + 'd ' + uptime_string[1] + 'h ' + uptime_string[2] + 'm ' + uptime_string[3] + 's'
            print(self.loaded_modules)
            module_string = ''
            for botModule in self.loaded_modules:
                module_string += botModule.name + ', '
            module_string = module_string[:-2]
            msg = '```\n Uptime: ' + uptime_string + '\n Loaded modules: ' + module_string + '\n```'
            await client.send_message(message.channel, msg)
