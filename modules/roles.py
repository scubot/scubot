import discord

rolesTriggerString = '!role'

async def parse_roles_command(message, client):
    msg = 'Role!'
    await client.send_message(message.channel, msg)
