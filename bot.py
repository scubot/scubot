import discord

from modules.units import *
from modules.roles import *

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        msg = 'Pong! This bot is alive.'
        await client.send_message(message.channel, msg)

    elif message.content.startswith(unitsTriggerString):
        await parse_units_command(message, client)
        
    elif message.content.startswith(rolesTriggerString):
        await parse_roles_command(message, client)


@client.event
async def on_ready():
    print('Logged in as')
    print('User:', client.user.name)
    print('ID', client.user.id)
    print('------')


tokenFile = open('token')
token = tokenFile.read().replace('\n', '')
client.run(token)
