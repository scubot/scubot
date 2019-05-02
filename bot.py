import sys
import traceback

import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix="?", description="scubot")
bot.version = "2.0.0"

config_path = "config.json"
token_path = "token.json"

if config_path:
    with open(config_path, 'r') as f:
        bot.configs = json.load(f)
else:
    print("[WARN] No config.json file found! Will try to continue loading.")

for x in bot.configs["load_modules"]:
    print("[LOAD] " + x)
    try:
        bot.load_extension(x)
    except Exception as e:
        print(e)
        print("[WARN] " + x + " could not be loaded. Skipping...")

print("All modules loaded.")

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
print("v" + bot.version)
print("Logging in...")


@bot.event
async def on_ready():
    print('Bot online as ' + str(bot.user))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):  # Command not found, not our fault.
        return
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):  # Missing some sort of argument - who knows?
        await ctx.send("[!] Missing required argument.")
        return
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("[!] I'm sorry " + ctx.author.name + ", I'm afraid I can't do that.")
        return
    if isinstance(error, discord.ext.commands.ExtensionError):
        return  # Already handled in loader

    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot.run(token)
