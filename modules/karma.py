import discord
from modules.botModule import *
import shlex
import time
import modules.reactionscroll as rs


class KarmaScrollable(rs.Scrollable):
    async def preprocess(self, client, module_db):
        ranked = sorted(module_db.all(), key=lambda k: k['karma'])[::-1]
        fallback_users = {}
        ret = []
        for item in ranked:
            user = discord.utils.get(client.get_all_members(), id=item['userid'])
            if not user:
                try:
                    user = fallback_users[item['userid']]
                except KeyError:
                    user = await client.get_user_info(item['userid'])
                    fallback_users[item['userid']] = user
            ret.append([user, item['karma']])
        return ret

    async def refresh(self, client, module_db):
        self.processed_data.clear()
        self.embeds.clear()
        self.processed_data = await self.preprocess(client, module_db)
        self.create_embeds()


class Karma(BotModule):
        name = 'karma'

        description = 'Monitors messages for reactions and adds karma accordingly.'

        help_text = 'This module has no callable functions'

        trigger_string = 'karma'

        module_version = '1.1.0'

        listen_for_reaction = True

        up_react = [':star:', '⭐', 'waitwhat']  # apparently some return as unicode emoji
        down_react = [':thumbsdown:', '👎', 'lionfish']

        cooldown_time = 30

        module_db = TinyDB('./modules/databases/' + name)

        message_returns = []

        scroll = KarmaScrollable(limit=5, color=0xc0fefe, table=module_db, title="Top users with karma", inline=False)

        async def contains_returns(self, message):
            for x in self.message_returns:
                if message.id == x[0].id:
                    return True
            return False

        async def find_pos(self, message):
            for x in self.message_returns:
                if message.id == x[0].id:
                    return x[1]

        async def update_pos(self, message, ty):
            for x in self.message_returns:
                if message.id == x[0].id:
                    if ty == 'next':
                        x[1] += 1
                    if ty == 'prev':
                        x[1] -= 1

        def cooled_down(self, userid):
            target_user = Query()
            time_now = int(time.time())
            cooldown = self.module_db.table('cooldown')
            if cooldown.get(target_user.userid == userid) is None:
                cooldown.insert({'userid': userid, 'lastreact': time_now})
                user_last_react = time_now - self.cooldown_time - 1 # This makes sure that a first time user will always get their first react
            else:
                user_last_react = cooldown.get(target_user.userid == userid)['lastreact']

            if time_now > user_last_react + self.cooldown_time:
                return True
            else:
                return False

        async def parse_command(self, message, client):
            await self.scroll.refresh(client, self.module_db)
            msg = shlex.split(message.content)
            target_user = Query()
            if len(msg) > 1:
                if msg[1] == 'reset':
                    self.module_db.update({'karma': 0}, target_user.userid == message.author.id)
                    msg = "[:ok_hand:] Your karma has been reset to 0."
                    await client.send_message(message.channel, msg)
                elif msg[1] == 'rank':
                    m_ret = await client.send_message(message.channel, embed=self.scroll.initial_embed())
                    self.message_returns.append([m_ret, 0])
                    await client.add_reaction(m_ret, "⏪")
                    await client.add_reaction(m_ret, "⏩")
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
            if react_text == "⏩" or react_text == "⏪":
                if not await self.contains_returns(reaction.message):
                    return 0
                pos = await self.find_pos(reaction.message)
                react_text = reaction.emoji
                if type(reaction.emoji) is not str:
                    react_text = reaction.emoji.name
                if react_text == "⏩":
                    embed = self.scroll.next(current_pos=pos)
                    await client.edit_message(reaction.message, embed=embed)
                    await self.update_pos(reaction.message, 'next')
                if react_text == "⏪":
                    embed = self.scroll.previous(current_pos=pos)
                    await client.edit_message(reaction.message, embed=embed)
                    await self.update_pos(reaction.message, 'prev')

            else:
                if self.cooled_down(user.id):
                    cooldown = self.module_db.table('cooldown')
                    time_now = int(time.time())

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

                        cooldown.update({'lastreact': time_now}, target_user.userid == user.id)

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
