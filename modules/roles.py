import discord
import shlex

rolesTriggerString = '!role'

async def parse_roles_command(message, client):
    msg = shlex.split(message.content)
    if len(msg) != 1
        await client.send_message(message.channel, msg[1])
    else:
        break
