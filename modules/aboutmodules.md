# Modules
The different modules in `scubot` allow it to perform multiple functions while keeping them separate. This allows for individual features to be added/removed with ease, or even disabled while keeping the module installed.

## Writing a module
Writing modules for the `scubot` is designed to be easy. Modules are stored in the `modules/` folder, and follow the naming rule of `name_of_feature.py` (e.g. `units.py` for converting between units and `roles.py` for assigning and managing roles).
#### The module itself
The module itself (`feature.py` in this case) looks like this:
```Python
import discord
from modules.botModule import BotModule
import ... # whatever is needed for your module

class Feature(BotModule):
    name = ''  # name of your module

    description = ''  # description of its function

    help_text = ''  # help text for explaining how to do things

    trigger_string = ''   # string to listen for as trigger

    async def parse_command(self, message, client):
        # do whatever to parse message and kick of rest of the work once the module is triggered

```
You should read `discord.py`'s documentation for more information.

#### Enabling and disabling modules
Now that you have a module, you should enable it (or disable it likewise) in `bot.py` (again, `feature.py` is used as an example):
```Python
import discord

from modules.units import *
#import your module
from modules.feature import *

# Add your module to the list of active modules
loaded_modules = [Units(), Feature()]

```

## FAQ:
#### My module doesn't work!
You should debug your module. The bot itself is written to be as barebones as possible, so the only thing that should go wrong are the modules. If you still think that the bot is broken, start an issue.
#### I made a module and I'd like it to be included in the default modules!
Send a PR in and it'll be looked at.
