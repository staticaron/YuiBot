from collections.abc import Callable

from discord import ButtonStyle, Interaction
from discord.ui import Button, View


class WarningView(View):
    def __init__(self, proceed_callback: Callable):
        super().__init__(timeout=60)
        self.proceed_callback_store = proceed_callback

        proceed_btn = Button(label="Proceed Anyway", style=ButtonStyle.grey)

        proceed_btn.callback = self.process_proceed_callback

        self.add_item(proceed_btn)

    async def process_proceed_callback(self, interaction: Interaction):
        await interaction.response.defer()
        await self.proceed_callback_store(interaction)

