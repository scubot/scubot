from collections import namedtuple
import re
import discord
from modules.botModule import BotModule


class Units(BotModule):
    name = 'units'

    description = 'Allow for the conversion between common units'

    help_text = 'This module supports two types of conversion, explicit and implicit. \n\n' \
                'Explicit conversion takes the form "!convert <number> <unit>" (e.g !convert 10 ft) and will post a ' \
                'conversion.\n\n' \
                ' Implicit conversion takes the form of "!convert" or "!convert all", this mode looks through the ' \
                'past 10 messages and converts the first unit it finds, by adding all it will convert all the units ' \
                'found in the past 10 messages.'

    trigger_string = 'convert'

    Unit = namedtuple("Unit", "name prefix conversionValue excludes")  # makeshift struct

    AvailableUnits = [Unit("pounds per square inch", "psi", 0.068947697587212, "default exclude"),
                      Unit("feet", "ft", 0.3048, "default exclude"),
                      Unit("meters", "m", 3.28084, "default exclude"),
                      Unit("pounds", "lbs", 0.453592, "pounds per square inch"),
                      Unit("kilograms", "kg", 2.20462, "default exclude"),
                      Unit("fathoms", "fsw", 1.8288, "default exclude"),
                      Unit("bar", "br", 14.5038, "default exclude")]

    UnitPairs = {'pounds per square inch': 'bar',
                 'bar': 'pounds per square inch',
                 'feet': 'meters',
                 'meters': 'feet',
                 'pounds': 'kilograms',
                 'kilograms': 'pounds',
                 'fathoms': 'meters'
                 }

    historyLimit = 10  # number of messages to search back for conversion

    module_version = '1.0.1'

    # This is where the fun begins

    async def parse_command(self, message, client):
        bulk = False
        channel = message.channel
        if 'all' in message.content:  # convert all recent messages rather than just the first one
            bulk = True
        if message.content.lower() == self.trigger_char + self.trigger_string or message.content == self.trigger_char + self.trigger_string + ' all':
            for msg in client.logs_from(channel, limit=self.historyLimit):
                for unit in self.AvailableUnits:
                    if msg.author != client.user:  # don't convert yourself
                        send_message = self.parse_units(msg, unit)

                        if send_message != '':  # returns empty when no match found (can't send empty message)
                            messages = send_message.split(',')  # send different conversions as different messages

                            for send in messages:
                                await client.send_message(message.channel, send)
                            if not bulk:
                                return  # break after 1 message unless bulk

        else:  # this is for explicit conversions (eg '!convert 10 ft')
            for unit in self.AvailableUnits:
                send_message = self.parse_units(message, unit)
                if send_message != '':  # returns empty when no match found (can't send empty message)
                    messages = send_message.split(',')  # send different conversions as different messages
                    for send in messages:
                        await client.send_message(message.channel, send)

    def parse_units(self, message, unit):
        if re.search('([0-9]|\.)+(| )(?!' + unit.excludes + ')(' + unit.prefix + '|' + unit.name + ')',
                     message.content) is not None:
            response = ''
            first_loop = True  # keep track of when to add commas
            message_regex = re.finditer(
                '([0-9]|\.)+(| )(?!' + unit.excludes + ')(' + unit.prefix + '|' + unit.name + ')', message.content)
            for match in message_regex:
                string = match.group(0)  # match group 0 is the message
                try:
                    current_value = float(string.replace(match.group(3), ''))  # group 3 is the unit suffix
                    converted_value = current_value * unit.conversionValue

                    if not first_loop:
                        response += ','  # we split up into multiple messages later
                    converted_string = str("{0:.2f}".format(converted_value))  # cast to string with 2 decimal places
                    response += string + ' is ' + converted_string + ' ' + self.UnitPairs[unit.name]
                    first_loop = False
                except:
                    response = 'Tried to convert invalid number: ' + string
            return response
        return ''
