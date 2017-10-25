import discord
from modules.botModule import BotModule

class Karma(BotModule):
        name = 'karma'

        description = 'Monitors messages for reactions and adds karma accordingly.'

        help_text = 'This module has no callable functions'

        trigger_string = '!reddit'

        module_db = 'karma.json'

        module_version = '0.1.0'

        listen_for_reaction = True

        async def parse_command(self, message, client):
            pass

        async def on_reaction(self, reaction, client):
            target_user = self.module_db.Query()
            if self.module_db.get(target_user.userid == reaction.message.author.id) == None:
                self.module_db.insert({'userid': reaction.message.author.id, 'karma': 1})

                msg = 'New entry for ' + reaction.message.author.id + ' added.'
                await client.send_message(reaction.message.channel, msg)
            else:
                new_karma = self.module_db.get(target_user.userid == reaction.message.author.id)['karma'] + 1
                self.module_db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)

                msg = 'Karma for ' + reaction.message.author.id + ' updated to ' + new_karma
                await client.send_message(reaction.message.channel, msg)

            #msg = "I saw that!" + reaction.message.author.name + reaction.emoji
            #await client.send_message(reaction.message.channel, msg)