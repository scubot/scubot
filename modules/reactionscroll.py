import discord
from modules.botModule import *
from tinydb import TinyDB, Query
import shlex
import time
import math

class Scrollable():
    # This object provides an easy way to turn a TinyDB table into a scrollable embed.
    # However, scrolling logic is not included in this object.
    def __init__(self, *, limit, color, table, title, inline):
        self.color = color
        self.limit = limit
        self.table = table
        self.title = title
        self.inline = inline
        self.embeds = []
        self.processed_data = []

    def preprocess(self, field):
        # By default this method will take the designated field and make a title, omitting 'description'.
        # You may want to override this default behaviour to suit your table's needs.
        # The resulting embeds will be created with the order than the list is returned in.
        # Should return a 2-dimensional list of [title, data].
        return [[x[field], 'Testing'] for x in self.table]

    def refresh(self, field):
        self.processed_data.clear()
        self.embeds.clear()
        self.processed_data = self.preprocess(field=field)
        self.create_embeds()

    def create_embeds(self):
        counter = 1
        page = 1
        for item in self.processed_data:
            page = math.ceil(counter/self.limit)
            if counter == 1:
                # Just started the loop -- make a new embed object
                embed = discord.Embed(title=self.title, color=self.color)
                embed.set_footer(text="Page " + str(page) + " of " + str(math.ceil(len(self.processed_data)/self.limit)))
                embed.add_field(name=item[0], value=item[1], inline=self.inline)
            elif counter % self.limit == 0:
                # Last one in this embed object, now append and make a new object
                embed.add_field(name=item[0], value=item[1], inline=self.inline)
                self.embeds.append(embed)
                del embed
                embed = discord.Embed(title=self.title, color=self.color)
                embed.set_footer(text="Page " + str(page+1) + " of " + str(math.ceil(len(self.processed_data)/self.limit)))
            elif counter == len(self.processed_data):
                # Last one in loop
                embed.add_field(name=item[0], value=item[1], inline=self.inline)
                self.embeds.append(embed)
                del embed
            else:
                # Else, nothing special needs to be done.
                embed.add_field(name=item[0], value=item[1], inline=self.inline)
            counter += 1

    def next(self, *, current_pos):
        return self.embeds[(int(current_pos) + 1) % len(self.embeds)]

    def previous(self, *, current_pos):
        return self.embeds[(int(current_pos) - 1) % len(self.embeds)]

    def initial_embed(self):
        return self.embeds[0]