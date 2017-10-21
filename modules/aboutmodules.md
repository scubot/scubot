# Modules
The different modules in `scubot` allow it to perform multiple functions while keeping them separate. This allows for individual features to be added/removed with ease, or even disabled while keeping the module installed.

## Writing a module
Writing modules for the `scubot` is designed to be easy. Modules are stored in the `modules/` folder, and follow the naming rule of `name_of_feature.py` (e.g. `units.py` for converting between units and `roles.py` for assigning and managing roles).
#### The module itself
The module itself (`feature.py` in this case) looks like this:
```Python
import discord
import ... # Import everything else you need

featureTriggerString = '!feature' # e.g. !convert

async def parse_feature_command(message,client):
# e.g. parse_units_command
  do_stuff()
  msg = "What you want to send, if any"
  await client.send_message(message.channel, send)
```
You should read `discord.py`'s documentation for more information.

#### Enabling and disabling modules
Now that you have a module, you should enable it (or disable it likewise) in `bot.py` (again, `feature.py` is used as an example):
```Python
import discord

from modules.units import *
from modules.feature import *
# Add or remove these lines to enable/disable individual modules

@client.event
async def on_message(message):
    ...
    elif message.content.startswith(unitsTriggerString):
        await parse_units_command(message, client)
    elif message.content.startswith(featureTriggerString):
        await parse_feature_command(message,client)
    # Add or remove the above 2 lines to enable/disable individual modules.
```

## FAQ:
#### My module doesn't work!
You should debug your module. The bot iself is written to be as barebones as possible, so the only thing that should go wrong are the modules. If you still think that the bot is broken, start an issue.
#### I made a module and I'd like it to be included in the default modules!
Send a PR in and it'll be looked at.
