import time

from discord.ext import commands
import discord
from discord.utils import find
from tinydb import *
import modules.reactionscroll as rs


class KarmaScrollable(rs.Scrollable):
    async def preprocess(self, bot, module_db):
        ranked = sorted(module_db.all(), key=lambda k: k['karma'])[::-1]
        ret = []
        for item in ranked:
            user = find(lambda o: o.id == item['userid'], list(bot.get_all_members()))
            if not user:
                ret.append(["User not found...", item['karma']])
            else:
                ret.append([user.name, item['karma']])
        return ret

    async def refresh(self, bot, module_db):
        self.processed_data.clear()
        self.embeds.clear()
        self.processed_data = await self.preprocess(bot, module_db)
        self.create_embeds()


class Karma(commands.Cog):
    up = [':star:', '⭐']  # apparently some return as unicode emoji
    down = ['lionfish']
    cooldown_time = 30

    scrolling_cache = []

    def __init__(self, bot):
        self.version = "2.0.1"
        self.bot = bot
        self.db = TinyDB('./modules/databases/karma')
        self.scroll = KarmaScrollable(limit=5, color=0xc0fefe, table=self.db, title="Top users with karma",
                                      inline=False)

    # Helper functions for scrolling
    async def contains_returns(self, message):
        for x in self.scrolling_cache:
            if message.id == x[0].id:
                return True
        return False

    async def find_pos(self, message):
        for x in self.scrolling_cache:
            if message.id == x[0].id:
                return x[1]

    async def update_pos(self, message, ty):
        for x in self.scrolling_cache:
            if message.id == x[0].id:
                if ty == 'next':
                    x[1] += 1
                if ty == 'prev':
                    x[1] -= 1

    def cooled_down(self, userid):
        target_user = Query()
        time_now = int(time.time())
        cooldown = self.db.table('cooldown')
        if cooldown.get(target_user.userid == userid) is None:
            cooldown.insert({'userid': userid, 'lastreact': time_now})
            # This makes sure that a first time user will always get their first react
            user_last_react = time_now - self.cooldown_time - 1
        else:
            user_last_react = cooldown.get(target_user.userid == userid)['lastreact']
        return time_now > user_last_react + self.cooldown_time

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add_karma(self, reaction, user):
        react_text = reaction.emoji
        if type(reaction.emoji) is not str:
            react_text = reaction.emoji.name
        if user.id == reaction.message.author.id:  # Cannot star/lionfish own message
            return

        if self.cooled_down(user.id):
            cooldown_table = self.db.table('cooldown')
            time_now = int(time.time())
            target_user = Query()
            if self.db.get(target_user.userid == reaction.message.author.id) is None:
                self.db.insert({'userid': reaction.message.author.id, 'karma': 0})
            if react_text in self.up:
                new_karma = self.db.get(target_user.userid == reaction.message.author.id)['karma'] + 1
                self.db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
            elif react_text in self.down:
                new_karma = self.db.get(target_user.userid == reaction.message.author.id)['karma'] - 1
                self.db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
            cooldown_table.update({'lastreact': time_now}, target_user.userid == user.id)

    @commands.Cog.listener("on_reaction_remove")
    async def on_reaction_remove_karma(self, reaction, user):
        react_text = reaction.emoji
        if type(reaction.emoji) is not str:
            react_text = reaction.emoji.name
        if user.id == reaction.message.author.id:  # Cannot star/lionfish own message
            return

        if self.cooled_down(user.id):
            cooldown_table = self.db.table('cooldown')
            time_now = int(time.time())
            target_user = Query()
            if self.db.get(target_user.userid == reaction.message.author.id) is None:
                self.db.insert({'userid': reaction.message.author.id, 'karma': 0})
            if react_text in self.up:
                new_karma = self.db.get(target_user.userid == reaction.message.author.id)['karma'] - 1
                self.db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
            elif react_text in self.down:
                new_karma = self.db.get(target_user.userid == reaction.message.author.id)['karma'] + 1
                self.db.update({'karma': new_karma}, target_user.userid == reaction.message.author.id)
            cooldown_table.update({'lastreact': time_now}, target_user.userid == user.id)

    @commands.group(invoke_without_command=True)
    async def karma(self, ctx):
        target_user = Query()
        if self.db.get(target_user.userid == ctx.author.id) is None:
            self.db.insert({'userid': ctx.author.id, 'karma': 0})
        user_karma = self.db.get(target_user.userid == ctx.author.id)['karma']
        msg = str(ctx.author) + "'s karma: " + str(user_karma)
        await ctx.send(msg)

    @karma.command(name="reset")
    async def reset(self, ctx):
        pass

    @karma.command(name="rank", aliases=['ranking', 'top'])
    async def rank(self, ctx):
        await self.scroll.refresh(self.bot, self.db)
        m = await ctx.send(embed=self.scroll.initial_embed())
        self.scrolling_cache.append([m, 0])
        await m.add_reaction("⏪")
        await m.add_reaction("⏩")

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add_scroll(self, reaction, user):
        if not await self.contains_returns(reaction.message):
            return
        pos = await self.find_pos(reaction.message)
        react_text = reaction.emoji
        if type(reaction.emoji) is not str:
            react_text = reaction.emoji.name
        if react_text == "⏩":
            embed = self.scroll.next(current_pos=pos)
            await reaction.message.edit(embed=embed)
            await self.update_pos(reaction.message, 'next')
        if react_text == "⏪":
            embed = self.scroll.previous(current_pos=pos)
            await reaction.message.edit(embed=embed)
            await self.update_pos(reaction.message, 'prev')


def setup(bot):
    bot.add_cog(Karma(bot))
