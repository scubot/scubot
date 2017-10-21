# TODO Put an enum matching unit pairs, will make code cleaner

import discord
import re
from unitconverter import *

client = discord.Client()


triggerString = '!convert'
historyLimit = 10

def construct_response(message_regex):
    string = message_regex.group(0) + ' is '
    current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
    converted_value = feet_to_meters(current_value)
    return string + str(converted_value)


def parse_units(message):
    if re.search('[0-9]+(| )(ft|feet)', message.content) is not None:
        msg = construct_response(re.search('[0-9]+(| )(ft|feet)', message.content)) + ' meters'
        return msg
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
        if message.content == triggerString:
            async for msg in client.logs_from(channel, limit=historyLimit):
                send_message = parse_units(msg)
                if send_message != '':
                    await client.send_message(message.channel, send_message)
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
