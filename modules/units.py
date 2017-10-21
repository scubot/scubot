from collections import namedtuple
import re
import discord

Unit = namedtuple("Unit", "name prefix conversionValue")

Units = [Unit("feet", "ft", 0.3048),
         Unit("meters", "m", 3.28084),
         Unit("pounds", "lbs", 0.453592),
         Unit("kilograms", "kg", 2.20462),
         Unit("fathoms", "fsw", 1.8288)]

UnitPairs = {'feet': 'meters',
             'meters': 'feet',
             'pounds': 'kilograms',
             'kilograms': 'pounds',
             'fathoms': 'meters'}

unitsTriggerString = '!convert'
historyLimit = 10


async def parse_units_command(message, client):
    bulk = False
    channel = message.channel
    if 'all' in message.content:
        bulk = True
    if message.content == unitsTriggerString or message.content == unitsTriggerString + ' all':
        async for msg in client.logs_from(channel, limit=historyLimit):
            for unit in Units:
                if msg.author != client.user:
                    send_message = parse_units(msg, unit)
                    if send_message != '':
                        messages = send_message.split(',')
                        for send in messages:
                            await client.send_message(message.channel, send)
                        if not bulk:
                            break
    else:
        for unit in Units:
            send_message = parse_units(message, unit)
            if send_message != '':
                messages = send_message.split(',')
                for send in messages:
                    await client.send_message(message.channel, send)


def parse_units(message, unit):
    if re.search('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content) is not None:
        response = ''
        loop_count = 0
        message_regex = re.finditer('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content)
        for match in message_regex:
            loop_count += 1
            string = match.group(0) + ' is '
            current_value = int(match.group(0).replace(match.group(2), ''))
            converted_value = current_value * unit.conversionValue
            if loop_count > 1:
                response += ','  # we split up into multiple messages later
            response += string + str("{0:.2f}".format(converted_value)) + ' ' + UnitPairs[unit.name]
        return response
    return ''
