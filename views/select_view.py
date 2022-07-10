from discord.ui import Button, View
from discord.ext import pages
from discord import ButtonStyle
from discord.ext.pages import PaginatorButton

from config import PREV_EMOTE, NEXT_EMOTE

class SelectView(View):

    def __init__(self, select_callback:callable, timeout:int=180):
        super().__init__(timeout=timeout)

        select_button:Button = Button(label="SELECT", style=ButtonStyle.green)
        self.add_item(select_button)

        select_button.callback = select_callback

class SelectPaginator(pages.Paginator):

    def __init__(self, pages:list, select_callback:callable):

        prev_btn:PaginatorButton = PaginatorButton("prev", None, PREV_EMOTE, ButtonStyle.blurple)
        next_btn:PaginatorButton = PaginatorButton("next", None, NEXT_EMOTE, ButtonStyle.blurple)

        buttons = []
        buttons.append(prev_btn)
        buttons.append(next_btn)

        super().__init__(pages, loop_pages=True, show_indicator=False, use_default_buttons=False, show_disabled=False, disable_on_timeout=True,custom_buttons=buttons, custom_view=SelectView(select_callback))
