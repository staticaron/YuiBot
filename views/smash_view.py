from discord import ButtonStyle, Interaction, Message
from discord.ui import Button, View


class SmashView(View):
    def __init__(self, message: Message, timeout: int = 180):
        super().__init__(timeout=timeout)

        self.message: Message = message

        smash_btn = Button(label="Smash", style=ButtonStyle.green)
        pass_btn = Button(label="Pass", style=ButtonStyle.gray)
        flush_btn = Button(label="Flush", style=ButtonStyle.red)

        smash_btn.callback = self.smash_callback
        pass_btn.callback = self.pass_callback
        flush_btn.callback = self.flush_callback

        self.add_item(smash_btn)
        self.add_item(pass_btn)
        self.add_item(flush_btn)

    async def smash_callback(self, interaction: Interaction):
        if interaction.user is None:
            return

        await interaction.response.send_message(
            f"{interaction.user.mention} will SMASH"
        )
        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

    async def pass_callback(self, interaction: Interaction):
        if interaction.user is None:
            return

        await interaction.response.send_message(f"{interaction.user.mention} will PASS")
        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

    async def flush_callback(self, interaction: Interaction):
        if interaction.user is None:
            return

        await interaction.response.send_message(
            f"{interaction.user.mention} will FLUSH"
        )
        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)

    async def on_timeout(self) -> None:
        await super().on_timeout()

        self.clear_items()
        await self.message.edit(content=self.message.content, view=self)
