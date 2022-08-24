from discord.ui import Button, View
from discord.ext import pages
from discord import Embed, ButtonStyle, Interaction
from discord.ext.pages import PaginatorButton

from config import PREV_EMOTE, NEXT_EMOTE


class SelectView(View):

    reply_callback: callable = None

    def __init__(self, reply_callable: callable, timeout: int = 30):
        super().__init__(timeout=timeout)

        self.reply_callback = reply_callable

        select_button: Button = Button(label="SELECT", style=ButtonStyle.green)
        self.add_item(select_button)

        select_button.callback = self.main_callback

    async def main_callback(self, interaction: Interaction):

        await interaction.response.defer()

        reply = await self.reply_callback()

        if isinstance(reply, Embed):
            await interaction.followup.send(embed=reply)
        elif isinstance(reply, pages.Paginator):
            await reply.respond(interaction)

class SelectPaginator(pages.Paginator):

    def __init__(self, pages: list, reply_callable: callable, timeout: int = 30):

        prev_btn: PaginatorButton = PaginatorButton(
            "prev", None, PREV_EMOTE, ButtonStyle.gray)
        next_btn: PaginatorButton = PaginatorButton(
            "next", None, NEXT_EMOTE, ButtonStyle.gray)

        buttons = []
        buttons.append(prev_btn)
        buttons.append(next_btn)

        super().__init__(pages, loop_pages=True, show_indicator=False, use_default_buttons=False, show_disabled=False,
                         disable_on_timeout=True, custom_buttons=buttons, custom_view=SelectView(reply_callable), timeout=timeout)
