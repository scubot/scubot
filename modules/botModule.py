class BotModule:
    name = ''  # name of your module

    description = ''  # description of its function

    help_text = ''  # help text for explaining how to do things

    trigger_string = ''  # string to listen for as trigger

    async def parse_command(self, message, client):
        raise NotImplementedError("Parse function not implemented in module:" + self.name)
