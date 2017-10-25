import discord
import requests
import asyncio
from modules.botModule import BotModule


class RedditPost(BotModule):
    name = 'RedditPost'  # name of your module

    description = 'RedditPost automatically posts recent posts on r/scuba'  # description of its function

    help_text = 'This module has no callable functions'  # help text for explaining how to do things

    trigger_string = '!reddit'  # string to listen for as trigger

    has_background_loop = True

    lastPostId = ''

    updateTime = 5  # minutes

    def __init__(self):
        data = self.get('scuba')
        self.lastPostId = data[0]['data']['id']

    async def parse_command(self, message, client):
        await client.send_message(message.channel, self.help_text + '. ' + self.description)

    def get(self, sub):
        # An loop here is needed because for some reason html.json()["data]["children"] fails for no reason sporadically
        # Therefore if you loop it, it will eventually pass and return data.
        while True:
            try:
                html = requests.get("https://www.reddit.com/r/" + sub + "/new.json")
                data = html.json()["data"]["children"]
                return data
            except:
                pass

    def is_selfpost(self, data):
        if "reddit.com" in data["url"] and not "np.reddit.com" in data["url"]:
            return True
        else:
            return False

    def is_preview(self, data):
        try:
            i = data["preview"]
            return True
        except:
            return False

    def determine(self, data):
        if self.is_selfpost(data):
            return 0
        elif self.is_preview(data):
            return 1
        else:
            return 3

    def truncate(self, text, width):
        from textwrap import shorten
        return shorten(text, width)

    def construct_embed(self, data, client):
        det = self.determine(data)
        if det == 0:
            description = self.truncate(data["selftext"], 1600)
            image_url = None
        elif det == 1:
            description = data["url"]
            image_url = data["preview"]["images"][0]["source"]["url"]
        elif det == 2:
            description = None
            image_url = data["url"]
        elif det == 3:
            description = data["url"]
            image_url = None

        embed = discord.Embed(title=self.truncate(data['title'], 255), description=description, colour=0xDEADBF)
        embed.set_author(name=self.truncate(data['author'], 255))
        embed.url = 'https://www.reddit.com' + data['permalink']
        if image_url is not None:
            embed.set_image(url=image_url)
        return embed

    async def background_loop(self, client):
        await client.wait_until_ready()
        channel = client.get_channel('371511262506385409')
        while not client.is_closed:
            embeds = []
            data = self.get('scuba')
            for post in data:
                post_data = post['data']
                if post_data['id'] == self.lastPostId:
                    break
                embeds.append(self.construct_embed(post_data, client))
            embeds.reverse()
            for embed in embeds:
                await client.send_message(channel, embed=embed)
            self.lastPostId = data[0]['data']['id']
            await asyncio.sleep(60)
