import discord
import math
from discord.ext import commands
from typing import List


class EmbedEntry:
    def __init__(self, title, content):
        self.title = title
        self.content = content


class EmbedChain:
    # Should pass a list of lists?
    def __init__(self, data: List[EmbedEntry], *, limit: int, color: int, title: str, inline: bool):
        self.contents = []
        self.current_position = 0
        # Literally copy-pasted this from reactionscroll...
        counter = 1
        page = 1
        embed = discord.Embed(title=title, color=color)
        embed.set_footer(
            text="Page " + str(page) + " of " + str(math.ceil(len(data) / limit)))
        for item in data:
            page = math.ceil(counter / limit)
            if counter % limit == 0:
                # Last one in this embed object, now append and make a new object
                embed.add_field(name=item.title, value=item.content, inline=inline)
                self.contents.append(embed)
                del embed
                embed = discord.Embed(title=title, color=color)
                embed.set_footer(
                    text="Page " + str(page + 1) + " of " + str(math.ceil(len(data) / limit)))
            elif counter == len(data):
                # Last one in loop
                embed.add_field(name=item.title, value=item.content, inline=inline)
                self.contents.append(embed)
                del embed
            else:
                # Else, nothing special needs to be done.
                embed.add_field(name=item.title, value=item.content, inline=inline)
            counter += 1

    def next(self) -> discord.Embed:
        self.current_position = (self.current_position + 1) % len(self.contents)
        return self.contents[self.current_position]

    def previous(self) -> discord.Embed:
        self.current_position = (self.current_position - 1) % len(self.contents)
        return self.contents[self.current_position]

    def current(self) -> discord.Embed:
        return self.contents[self.current_position]


class Dispatcher(commands.Cog):
    tracker = {}

    def __init__(self, bot):
        self.version = "0.1.0"
        self.bot = bot

    async def register(self, message: discord.Message, embed: EmbedChain):
        self.tracker[message.id] = embed
        await message.add_reaction("\U000023ea")
        await message.add_reaction("\U000023e9")

    async def deregister(self, message: discord.Message):
        self.tracker.pop(message)

    async def embed_update(self, message: discord.Message, new_embed: EmbedChain):
        self.tracker[message.id] = new_embed

    async def reaction_update(self, reaction):
        if reaction.me:
            return
        if reaction.message.id not in self.tracker:
            return
        embed = self.tracker[reaction.message.id]
        react_text = reaction.emoji
        if type(reaction.emoji) is not str:
            react_text = reaction.emoji.name
        if react_text == "⏩":
            embed = embed.next()
            await reaction.message.edit(embed=embed)
        if react_text == "⏪":
            embed = embed.previous()
            await reaction.message.edit(embed=embed)

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add_scroll(self, reaction, user):
        await self.reaction_update(reaction)

    @commands.Cog.listener("on_reaction_remove")
    async def on_reaction_remove_scroll(self, reaction, user):
        await self.reaction_update(reaction)


def setup(bot):
    bot.add_cog(Dispatcher(bot))
