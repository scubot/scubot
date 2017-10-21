# TODO Put an enum matching unit pairs, will make code cleaner

import discord
import re
from unitconverter import *

client = discord.Client()


triggerString = '!convert'
historyLimit = 10


def parse_units(message):
    if re.search('[0-9]+(| )(ft|feet)', message.content) is not None:
        message_regex = re.search('[0-9]+(| )(ft|feet)', message.content)
        string = message_regex.group(0) + ' is '
        current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
        converted_value = feet_to_meters(current_value)
        return string + str(converted_value) + ' meters'

    if re.search('[0-9]+(| )(m|meters)', message.content) is not None:
        message_regex = re.search('[0-9]+(| )(m|meters)', message.content)
        string = message_regex.group(0) + ' is '
        current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
        converted_value = meters_to_feet(current_value)
        return string + str(converted_value) + ' feet'

    if re.search('[0-9]+(| )(lbs|pounds)', message.content) is not None:
        message_regex = re.search('[0-9]+(| )(lbs|pounds)', message.content)
        string = message_regex.group(0) + ' is '
        current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
        converted_value = pounds_to_kilograms(current_value)
        return string + str(converted_value) + ' kilograms'

    if re.search('[0-9]+(| )(kg|kilograms)', message.content) is not None:
        message_regex = re.search('[0-9]+(| )(kg|kilograms)', message.content)
        string = message_regex.group(0) + ' is '
        current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
        converted_value = kilograms_to_pounds(current_value)
        return string + str(converted_value) + ' pounds'

    else:
        return ''


@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        msg = 'Pong! This bot is alive.'
        await client.send_message(message.channel, msg)

    elif message.content.startswith(triggerString):
        bulk = False
        if 'all' in message.content:
            bulk = True
        if message.content == triggerString or message.content == triggerString + ' all':
            async for msg in client.logs_from(channel, limit=historyLimit):
                if msg.author != client.user:
                    send_message = parse_units(msg)
                    if send_message != '':
                        await client.send_message(message.channel, send_message)
                        if not bulk:
                            break
        else:
            parse_units(message)
    else:
        previousMessage = message


@client.event
async def on_ready():
    print('Logged in as')
    print('User:', client.user.name)
    print('ID', client.user.id)
    print('------')


tokenFile = open('token')
token = tokenFile.read().replace('\n', '')
client.run(token)
