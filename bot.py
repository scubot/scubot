import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix="?", description="scubot")
info_path = "info.json"
token_path = "token.json"

startup_modules = ['modules.status']
for x in startup_modules:
    print("[LOAD] " + x)
    bot.load_extension(x)
print("All modules loaded.")


@bot.event
async def on_ready():
    print('Bot online as ' + str(bot.user))
    print('')


if info_path:
    with open(info_path, 'r') as f:
        info = json.load(f)


if token_path:
    with open(token_path, 'r') as g:
        token = json.load(g)["token"]
else:
    print("Token location not specified... Quiting")
if not token:
    print("No token found. Please put your token in token.json...")
    quit()

print("..######...######..##.....##.########...#######..########\n"
      ".##....##.##....##.##.....##.##.....##.##.....##....##...\n"
      ".##.......##.......##.....##.##.....##.##.....##....##...\n"
      "..######..##.......##.....##.########..##.....##....##...\n"
      ".......##.##.......##.....##.##.....##.##.....##....##...\n"
      ".##....##.##....##.##.....##.##.....##.##.....##....##...\n"
      "..######...######...#######..########...#######.....##...")
print("----------------------------------------------------------")
print("Logging in...")

bot.run(token)
