# TODO Put an enum matching unit pairs, will make code cleaner

import discord
import re
from unitconverter import *

client = discord.Client()


def construct_response(messageregex):
    string = messageregex.string + ' is '
    currentvalue = int(messageregex.string.replace(messageregex.group(2), ''))
    convertedvalue = feet_to_meters(currentvalue)
    return string + str(convertedvalue)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        msg = 'Pong! This bot is alive.'
        await client.send_message(message.channel, msg)

    # this technique can be used for the other units
    if re.search('[0-9]+(| )(ft|feet)', message.content) is not None:
        msg = construct_response(re.search('[0-9]+(| )(ft|feet)', message.content)) + ' meters'
        await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print('User:', client.user.name)
    print('ID', client.user.id)
    print('------')


tokenfile = open('token')
token = tokenfile.read().replace('\n', '')
client.run(token)
