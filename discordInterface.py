from time import sleep


class discordInterface():

    client = None

    Active = True

    SentRedundancyMessage = False

    RedundancyDelay = 60  # time between redundnacy checks in seconds (represents maximum time between failure and recovery)

    RedundancyInitiationMessage = "Redundancy handover initiation, if you are seeing this please open an issue at " \
                                  "www.github.com/scubot/scubot"

    RedundancyConfirmationMessage = "Redundancy handover confirmation, if you are seeing this please open an issue at " \
                                    "www.github.com/scubot/scubot"

    def __init(self, client):
        self.client = client

    def check_redundancy(self):
        self.client.send_message(self.client.user, self.RedundancyInitiationMessage)
        global Active
        global SentRedundancyMessage
        SentRedundancyMessage = True

    async def redundancy_handover_timer(self):
        sleep(self.RedundancyDelay)
        self.check_redundancy()

    async def send_message(self, content, target, is_embed):
        if not self.Active:
            return
        if is_embed:
            self.client.send_message(target, embed=content)
        else:
            self.client.send_message(target, content)

    async def add_roles(self, user, role):
        if not self.Active:
            return
        await self.client.add_roles(user, role)

    async def remove_roles(self, user, role):
        if not self.Active:
            return
        await self.client.remove_roles(user, role)