import discord
from tinydb import TinyDB, Query
from modules.botModule import BotModule
import shlex


class Karma(BotModule):
        name = 'karma'

        description = 'Monitors messages for reactions and adds karma accordingly.'

        help_text = 'This module has no callable functions'

        trigger_string = '!karma'

        module_version = '1.0.0'

        listen_for_reaction = True

        reaction_emojis = [':star:', '⭐', 'waitwhat']  # apparently some return as unicode emoji

        async def parse_command(self, message, client):
            msg = shlex.split(message.content)
            target_user = Query()
            if len(msg) > 1:
                if msg[1] == 'reset':
                    self.module_db.update({'karma': 0}, target_user.userid == message.author.id)
                    msg = "[:ok_hand:] Your karma has been reset to 0."
                    await client.send_message(message.channel, msg)
                else:
                    pass
            else:
                if self.module_db.get(target_user.userid == message.author.id) is None:
                    self.module_db.insert({'userid': message.author.id, 'karma': 0})
                user_karma = self.module_db.get(target_user.userid == message.author.id)['karma']
                msg = message.author.name + "'s karma: " + str(user_karma)
                await client.send_message(message.channel, msg)

        async def on_reaction_add(self, reaction, client, user):
            if reaction.emoji in self.reaction_emojis or reaction.emoji.name in self.reaction_emojis:
                target_user = Query()
                rlist = []
                for x in reaction.message.reactions[
                         :-1]:  # Check if person who reacted has already reacted to this message
                    for u in await client.get_reaction_users(x):
                        rlist.append(u)
                if user not in rlist:  # and reaction.message.author != user:  # DISABLE DURING DEVELOPMENT
                    if self.module_db.get(target_user.userid == reaction.message.author.id) is None:
                        self.module_db.insert({'userid': reaction.message.author.id, 'karma': 1})
                    else:
                        new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] + 1
                        self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
                else:
                    pass

        async def on_reaction_remove(self, reaction, client, user):
            if reaction.emoji in self.reaction_emojis:
                target_user = Query()
                if reaction.message.author != user:  # DISABLE DURING DEVELOPMENT
                    if self.module_db.get(target_user.userid == reaction.message.author.id) is None:
                        self.module_db.insert({'userid': reaction.message.author.id, 'karma': 0})
                    else:
                        new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] - 1
                        self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
                else:
                    pass
