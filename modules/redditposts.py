import discord
import requests
import json
from time import sleep

lastPostId = ''

updateTime = 5  # minutes


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


def is_selfpost(data):
    if "reddit.com" in data["url"] and not "np.reddit.com" in data["url"]:
        return True
    else:
        return False


def is_preview(data):
    try:
        i = data["preview"]
        return True
    except:
        return False


def determine(data):
    if is_selfpost(data):
        return 0
    elif is_preview(data):
        return 1
    else:
        return 3


def truncate(text):
    from textwrap import shorten
    return shorten(text, 1600)


def construct_embed(data, client):
    det = determine(data)
    if det == 0:
        description = truncate(data["selftext"])
        imageurl = None
    elif det == 1:
        description = data["url"]
        imageurl = data["preview"]["images"][0]["source"]["url"]
    elif det == 2:
        description = None
        imageurl = data["url"]
    elif det == 3:
        description = data["url"]
        imageurl = None

    embed = discord.Embed(title=data['title'], description=description, colour=0xDEADBF)
    embed.set_author(name=data['author'])
    embed.url = data['url']
    if imageurl is not None:
        embed.set_image(url=imageurl)
    return embed


async def reddit_check_and_post_loop(client):
    global lastPostId
    channel = client.get_channel('371511262506385409')
    while True:
        embeds = []
        data = get('scuba')
        for post in data:
            post_data = post['data']
            if post_data['id'] == lastPostId:
                break
            embeds.append(construct_embed(post_data, client))
        embeds.reverse()
        for embed in embeds:
            await client.send_message(channel, embed=embed)
        lastPostId = data[0]['data']['id']
        sleep(updateTime * 60)
