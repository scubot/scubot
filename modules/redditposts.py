import discord
import requests
import json
from time import sleep

redditPostsTriggerString = '!reddit'  # e.g. !convert

lastPostId = ''


def get(sub):
    # An loop here is needed because for some reason html.json()["data]["children"] fails for no reason sporadically
    # Therefore if you loop it, it will eventually pass and return data.
    while True:
        try:
            html = requests.get("https://www.reddit.com/r/" + sub + "/new.json")
            data = html.json()["data"]["children"]
            return data
        except:
            pass


async def parse_reddit_post_command(message, client):
    data = get('scuba')
    most_recent_post = data[0]['data']
    if most_recent_post['id'] == lastPostId:
        return
    await client.send_message(message.channel, most_recent_post['url'])
