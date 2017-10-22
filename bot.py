import discord

from modules.units import *
from modules.roles import *
from modules.help import *

client = discord.Client()

loaded_modules = [Units(), Roles()]

loaded_modules.append(Help(loaded_modules))  # needs access to the loaded modules list so is loaded later


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for bot_module in loaded_modules:
        if message.content.startswith(bot_module.trigger_string):
            await bot_module.parse_command(message, client)


@client.event
async def on_ready():
    print('Logged in as')
    print('User:', client.user.name)
    print('ID', client.user.id)
    print('------')

tokenFile = open('token')
token = tokenFile.read().replace('\n', '')
client.run(token)
