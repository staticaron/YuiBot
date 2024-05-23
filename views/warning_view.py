from discord import ButtonStyle
from discord.ui import View, Button
from discord import Interaction

class WarningView(View):

    proceed_callback_store = None

    def __init__(self, proceed_callback:callable):
        super().__init__(timeout=60)
        self.proceed_callback_store = proceed_callback

        proceed_btn = Button(label="Proceed Anyway", style=ButtonStyle.grey)

        proceed_btn.callback = self.process_proceed_callback

        self.add_item(proceed_btn)

    async def process_proceed_callback(self, interaction:Interaction):
        
        await interaction.response.defer()
        
        await self.proceed_callback_store(interaction)