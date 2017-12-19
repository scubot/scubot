import discord
from modules.botModule import *
import shlex


class Karma(BotModule):
        name = 'karma'

        description = 'Monitors messages for reactions and adds karma accordingly.'

        help_text = 'This module has no callable functions'

        trigger_string = 'karma'

        module_version = '1.1.0'

        listen_for_reaction = True

        up_react = [':star:', '⭐', 'waitwhat']  # apparently some return as unicode emoji
        down_react = [':thumbsdown:', '👎', 'lionfish']

        ranking_number = 5

        ranking_embed_colour = 0xc0fefe

        async def parse_command(self, message, client):
            msg = shlex.split(message.content)
            target_user = Query()
            if len(msg) > 1:
                if msg[1] == 'reset':
                    self.module_db.update({'karma': 0}, target_user.userid == message.author.id)
                    msg = "[:ok_hand:] Your karma has been reset to 0."
                    await client.send_message(message.channel, msg)
                elif msg[1] == 'rank':
                    text = ''
                    ranked = sorted(self.module_db.all(), key=lambda k: k['karma'])[:self.ranking_number]
                    ranked = ranked[::-1]
                    for entry in ranked:
                        user_entry = message.server.get_member(entry['userid'])
                        if user_entry is None:
                            username = 'Unknown user'
                        else:
                            username = user_entry.name
                        text += username + ': ' + str(entry['karma']) + '\n'
                    embed = discord.Embed(title='Overview', description=text, colour=self.ranking_embed_colour)
                    await client.send_message(message.channel, embed=embed)
                else:
                    pass
            else:
                if self.module_db.get(target_user.userid == message.author.id) is None:
                    self.module_db.insert({'userid': message.author.id, 'karma': 0})
                user_karma = self.module_db.get(target_user.userid == message.author.id)['karma']
                msg = message.author.name + "'s karma: " + str(user_karma)
                await client.send_message(message.channel, msg)

        async def on_reaction_add(self, reaction, client, user):
            react_text = reaction.emoji

            if type(reaction.emoji) is not str:
                react_text = reaction.emoji.name

            target_user = Query()
            rlist = []

            for x in reaction.message.reactions[
                     :-1]:  # Check if person who reacted has already reacted to this message
                for u in await client.get_reaction_users(x):
                    rlist.append(u)
            if user not in rlist and reaction.message.author != user:  # DISABLE DURING DEVELOPMENT
                if self.module_db.get(target_user.userid == reaction.message.author.id) is None:
                    self.module_db.insert({'userid': reaction.message.author.id, 'karma': 1})

                if react_text in self.up_react:
                    new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] + 1
                    self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)

                if react_text in self.down_react:
                    new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] - 1
                    self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
            else:
                pass

        async def on_reaction_remove(self, reaction, client, user):
            react_text = reaction.emoji

            if type(reaction.emoji) is not str:
                react_text = reaction.emoji.name

            target_user = Query()

            if reaction.message.author != user:  # DISABLE DURING DEVELOPMENT
                if self.module_db.get(target_user.userid == reaction.message.author.id) is None:
                    self.module_db.insert({'userid': reaction.message.author.id, 'karma': 0})

                if react_text in self.up_react:
                    new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] - 1
                    self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)

                if react_text in self.down_react:
                    new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] + 1
                    self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
            else:
                pass
