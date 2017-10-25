# Modules
The different modules in `scubot` allow it to perform multiple functions while keeping them separate. This allows for individual features to be added/removed with ease, or even disabled while keeping the module installed.

## Writing a simple module
Writing modules for the `scubot` is designed to be easy. Modules are stored in the `modules/` folder, and follow the naming rule of `name_of_feature.py` (e.g. `units.py` for converting between units and `roles.py` for assigning and managing roles). A module must implement `async def parse_command(self, message, client):` and `trigger_string` in order to get run properly, the other properties are optional but highly recommended.
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
BotModule.loaded_modules = [Units(), Feature()]

```

## Module methods and properties in detail
### Name
The name property is a short name used to identify your module when being accessed indirectly though commands like `!help`.
### Description
This property is currently unused but will become part of the help module and should properly describe what your module does and how it interacts with other services.
### help\_text
This property is used by the help module in order to provide usage information to the user, this should should state what commands your module takes and how it responds (it is recommended to include examples)
### trigger\_string
This is the string that your module will listen for when a message is received.
### loaded\_modules
This property is a list of all the currently loaded modules, and can be used for accessing other modules or checking dependencies.
### has\_background\_loop
This defines whether the module has a background loop that needs to be added to the event loop
### module_db
This is a [TinyDB](https://pypi.python.org/pypi/tinydb) object that links to `./modules/databases/<module name>.json` and is used for a modules permanent storage.
### parse\_command(message, client)
This is where code for handling messages goes, it only gets run if the message strts with the modules trigger\_string, the client parameter allows for the sending of messages in response or other tasks, see discord.py documentation for more details.
### background\_loop(client)
This is for creating loops for running in the background, an scafhold of a loop function is as follows:
``` Python
async def background_loop(self, client):
    await client.wait_until_ready()
    while not client.is_closed:
        # loop content goes here
```
If using a loop make sure to set has\_background\_loop to `True` in the module class.

## FAQ
### My module doesn't work!
You should debug your module. The bot itself is written to be as barebones as possible, so the only thing that should go wrong are the modules. If you still think that the bot is broken, start an issue.
### I made a module and I'd like it to be included in the default modules!
Send a PR in and it'll be looked at.
