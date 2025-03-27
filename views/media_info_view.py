from discord.ui import View, Button
from discord import ButtonStyle, Interaction, Embed

class MediaInfoView(View):

    details_embd:Embed = None
    tags_embd:Embed = None

    def __init__(self, embeds:dict[str, Embed], timeout:int=1000):
        super().__init__(timeout=timeout)

        self.details_embd = embeds.get("details")
        self.tags_embd = embeds.get("tags")

        details_btn = Button(label="Details", style=ButtonStyle.gray)
        tags_btn = Button(label="Tags", style=ButtonStyle.gray)

        details_btn.callback = self.details_callback
        tags_btn.callback = self.tags_callback

        self.add_item(details_btn)
        self.add_item(tags_btn)

    async def details_callback(self, interaction:Interaction) -> None:
        await interaction.response.edit_message(embed=self.details_embd, view=self)

    async def tags_callback(self, interaction:Interaction) -> None:
        await interaction.response.edit_message(embed=self.tags_embd, view=self)

