import time

from discord.ext import commands
import discord
from tinydb import *


class Karma(commands.Cog):
    up = [':star:', '⭐']  # apparently some return as unicode emoji
    down = ['lionfish']
    cooldown_time = 30

    def __init__(self, bot):
        self.version = "2.0.0"
        self.bot = bot
        self.db = TinyDB('./modules/databases/karma')

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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
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

    @commands.command()
    async def karma(self, ctx, reset: str = None):
        if reset == "reset":
            # reset karma
            pass
        target_user = Query()
        if self.db.get(target_user.userid == ctx.author.id) is None:
            self.db.insert({'userid': ctx.author.id, 'karma': 0})
        user_karma = self.db.get(target_user.userid == ctx.author.id)['karma']
        msg = str(ctx.author) + "'s karma: " + str(user_karma)
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Karma(bot))
