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
            if msg.author != client.user:
                send_message = parse_units(msg)
                if send_message != '':
                    await client.send_message(message.channel, send_message)
                    if not bulk:
                        break
    else:
        send_message = parse_units(message)
        await client.send_message(message.channel, send_message)


def parse_units(message):
    for unit in Units:
        if re.search('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content) is not None:
            message_regex = re.search('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content)
            string = message_regex.group(0) + ' is '
            current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
            converted_value = current_value * unit.conversionValue
            return string + str("{0:.2f}".format(converted_value)) + ' ' + UnitPairs[unit.name]
    return ''
