class BotModule:
    name = ''  # name of your module

    description = ''  # description of its function

    help_text = ''  # help text for explaining how to do things

    trigger_string = ''  # string to listen for as trigger

    has_background_loop = False

    listen_for_reaction = False

    loaded_modules = []

    bot_version = '0.1.0'

    async def parse_command(self, message, client):
        raise NotImplementedError("Parse function not implemented in module:" + self.name)

    async def background_loop(self, client):
        raise NotImplementedError("background_loop function not implemented in module:" + self.name)

    async def on_reaction(self, reaction, client):
        raise NotImplementedError("background_loop function not implemented in module:" + self.name)
