import discord
import re
from unitconverter import *

client = discord.Client()

triggerString = '!convert'
historyLimit = 10


def parse_units(message):
    for unit in Units:
        if re.search('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content) is not None:
            message_regex = re.search('[0-9]+(| )(' + unit.prefix + '|' + unit.name + ')', message.content)
            string = message_regex.group(0) + ' is '
            current_value = int(message_regex.group(0).replace(message_regex.group(2), ''))
            converted_value = current_value * unit.conversionValue
            return string + str("{0:.2f}".format(converted_value)) + ' ' + UnitPairs[unit.name]
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
            send_message = parse_units(message)
            await client.send_message(message.channel, send_message)


@client.event
async def on_ready():
    print('Logged in as')
    print('User:', client.user.name)
    print('ID', client.user.id)
    print('------')


tokenFile = open('token')
token = tokenFile.read().replace('\n', '')
client.run(token)
