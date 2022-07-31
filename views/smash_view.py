from discord.ui import View, Button
from discord import ButtonStyle, Message, Interaction

class SmashView(View):

    message = None

    def __init__(self, message:Message, timeout:int=180):
        super().__init__(timeout=timeout)

        self.message = message

        smash_btn = Button(label="Smash", style=ButtonStyle.green)
        pass_btn = Button(label="Pass", style=ButtonStyle.gray)
        flush_btn = Button(label="Flush", style=ButtonStyle.red)

        smash_btn.callback = self.smash_callback
        pass_btn.callback = self.pass_callback
        flush_btn.callback = self.flush_callback

        self.add_item(smash_btn)
        self.add_item(pass_btn)
        self.add_item(flush_btn)

    async def smash_callback(self, interaction:Interaction):

        await interaction.response.send_message("{} will SMASH".format(interaction.user.mention))
        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

    async def pass_callback(self, interaction:Interaction):

        await interaction.response.send_message("{} will PASS".format(interaction.user.mention))
        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

    async def flush_callback(self, interaction:Interaction):

        await interaction.response.send_message("{} will FLUSH".format(interaction.user.mention))   
        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

    async def on_timeout(self) -> None:
        await super().on_timeout()

        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

