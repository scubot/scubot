import discord

from modules.units import *
from modules.roles import *
from modules.help import *
from modules.status import *
from modules.redditposts import *
from modules.karma import *
from modules.info import *
from modules.deco.deco import *


from modules.botModule import *

client = discord.Client()

bot_version = '1.1.0'

BotModule.loaded_modules = [Units(), Roles(), Help(), Status(bot_version), Karma(), Info(), Deco()]  # Reddit module removed as it prevented startup


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for bot_module in BotModule.loaded_modules:
        if message.content.startswith(bot_module.trigger_char + bot_module.trigger_string):
            await bot_module.parse_command(message, client)
    for bot_module in BotModule.loaded_modules:
        if bot_module.trigger_on_mention and message.mentions:
            await bot_module.on_mention(message, client)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    for bot_module in BotModule.loaded_modules:
        if bot_module.listen_for_reaction:
            await bot_module.on_reaction_add(reaction, client, user)


@client.event
async def on_reaction_remove(reaction, user):
    if user == client.user:
        return
    for bot_module in BotModule.loaded_modules:
        if bot_module.listen_for_reaction:
            await bot_module.on_reaction_remove(reaction, client, user)


@client.event
async def on_ready():
    print('Login success. Your details:')
    print('User:', client.user.name)
    print('ID', client.user.id)
    print('----------')


print('scubot v' + bot_version)
try:
    tokenFile = open('token')
except FileNotFoundError:
    print('Token not found. Please make sure you have a token file in this directory.'
          ' Refer to README.md for details on getting a token.')
    quit()
print('Token found. Logging in...')
token = tokenFile.read().replace('\n', '')

for bot_module in BotModule.loaded_modules:
    if bot_module.has_background_loop:
        client.loop.create_task(bot_module.background_loop(client))

client.run(token)
