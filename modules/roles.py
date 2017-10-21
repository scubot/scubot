import discord
import shlex

rolesTriggerString = '!role'

async def parse_roles_command(message, client):
    server_roles = message.server.roles
    server_roles_str = [x.name for x in server_roles]
    msg = shlex.split(message.content)
    role = [i for i,x in enumerate(server_roles_str) if x == msg[1]]
    if len(msg) != 1:
        try:
            await client.add_roles(message.author,message.server.roles[role[0]])
        except discord.DiscordException:
            msg = "I'm sorry " + message.author.name + " ,I'm afraid I can't do that."
            client.send_message(message.channel, msg)
    else:
        pass
