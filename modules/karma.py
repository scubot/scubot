import time
from discord.utils import find
from tinydb import *
from modules.dispatch import *
from modules.dispatch import EmbedEntry
from util.missingdependency import MissingDependencyException


class Karma(commands.Cog):
    up = [':star:', '⭐']  # apparently some return as unicode emoji
    down = ['lionfish']
    cooldown_time = 30

    scrolling_cache = []

    def __init__(self, bot):
        self.version = "2.0.3"
        self.bot = bot
        self.db = TinyDB('./modules/databases/karma')
        self.dispatcher = bot.get_cog("Dispatcher")

    async def make_rank_entries(self) -> List[EmbedEntry]:
        ranked = sorted(self.db.all(), key=lambda k: k['karma'])[::-1]
        ret: List[EmbedEntry] = []
        for item in ranked:
            user = find(lambda o: o.id == item['userid'], list(self.bot.get_all_members()))
            if not user:
                ret.append(EmbedEntry("User not found...", item['karma']))
            else:
                ret.append(EmbedEntry(user.name, item['karma']))
        return ret

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
        embed: EmbedChain = EmbedChain(await self.make_rank_entries(), limit=5, color=0xc0fefe,
                                       title="Top users with karma", inline=False)
        await self.dispatcher.register(await ctx.send(embed=embed.current()), embed)


def setup(bot):
    if not bot.get_cog("Dispatcher"):
        raise MissingDependencyException("Dispatcher")
    bot.add_cog(Karma(bot))
