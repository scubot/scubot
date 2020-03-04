import sys
import traceback

import discord
from discord.ext import commands
import json


PREFIX = "!"
DESCRIPTION = "scubot"
BOT_VERSION = "2.1.0"
CONFIG_PATH = "config.json"
TOKEN_PATH = "token.json"


try:
    with open(CONFIG_PATH, 'r') as fp:
        config = json.load(fp)
        modules_to_load = config["load_modules"]
except FileNotFoundError:
    print("[FATAL] No config.json file found. Startup aborted.")
    sys.exit()

try:
    with open(TOKEN_PATH, 'r') as fp:
        token = json.load(fp)["token"]
except FileNotFoundError:
    print("[FATAL] No token file found. Startup aborted.")
    sys.exit()

print("""
----------------------------------------------------------
..######...######..##.....##.########...#######..########
.##....##.##....##.##.....##.##.....##.##.....##....##...
.##.......##.......##.....##.##.....##.##.....##....##...
..######..##.......##.....##.########..##.....##....##...
.......##.##.......##.....##.##.....##.##.....##....##...
.##....##.##....##.##.....##.##.....##.##.....##....##...
..######...######...#######..########...#######.....##...
----------------------------------------------------------
""")
print(f"v{BOT_VERSION}")
print("Logging in...")


def run_bot():
    bot = commands.Bot(command_prefix=PREFIX, description=DESCRIPTION, case_insensitive=True)
    bot.version = BOT_VERSION
    if len(modules_to_load) != 0:
        for module in modules_to_load:
            try:
                bot.load_extension(module)
                print(f"[LOAD] Successfully loaded extension {module}")
            except Exception as e:
                print(e)
                print(f"[ERROR] Failed to load extension {module}, continuing.")
    bot.run(token)


if __name__ == '__main__':
    run_bot()
