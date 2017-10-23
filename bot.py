import discord

from modules.units import *
from modules.roles import *
from modules.help import *
from modules.status import *

from modules.botModule import *

client = discord.Client()

BotModule.loaded_modules = [Units(), Roles(), Help(), Status()]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for bot_module in BotModule.loaded_modules:
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
