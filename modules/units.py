from collections import namedtuple
import re
import discord

Unit = namedtuple("Unit", "name prefix conversionValue")  # makeshift struct

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

unitsTriggerString = '!convert'  # string to listen for as trigger
historyLimit = 10  # number of messages to search back for conversion


# This is where the fun begins


async def parse_units_command(message, client):
    bulk = False
    channel = message.channel
    if 'all' in message.content:  # convert all recent messages rather than just the first one
        bulk = True
    if message.content == unitsTriggerString or message.content == unitsTriggerString + ' all':  # bad, should change
        async for msg in client.logs_from(channel, limit=historyLimit):
            for unit in Units:
                if msg.author != client.user:  # don't convert yourself
                    send_message = parse_units(msg, unit)

                    if send_message != '':  # returns empty when no match found (can't send empty message)
                        messages = send_message.split(',')  # send different conversions as different messages

                        for send in messages:
                            await client.send_message(message.channel, send)
                        if not bulk:
                            break  # break after 1 message unless bulk

    else:  # this is for explicit conversions (eg '!convert 10 ft')
        for unit in Units:
            send_message = parse_units(message, unit)
            if send_message != '':  # returns empty when no match found (can't send empty message)
                messages = send_message.split(',')  # send different conversions as different messages
                for send in messages:
                    await client.send_message(message.channel, send)


def parse_units(message, unit):
    if re.search('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content) is not None:
        response = ''
        first_loop = True  # keep track of when to add commas
        message_regex = re.finditer('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content)

        for match in message_regex:
            string = match.group(0) + ' is '  # match group 0 is the entire matched area
            current_value = int(match.group(0).replace(match.group(2), ''))  # group 2 is the unit suffix
            converted_value = current_value * unit.conversionValue

            if not first_loop:
                response += ','  # we split up into multiple messages later
            converted_string = str("{0:.2f}".format(converted_value))  # cast to string with 2 decimal places
            response += string + converted_string + ' ' + UnitPairs[unit.name]
            first_loop = False
        return response
    return ''
