from discord import ButtonStyle
from discord.ext import pages
from discord.ext.pages import PaginatorButton

from config import PREV_EMOTE, NEXT_EMOTE

class Scroller(pages.Paginator):

    def __init__(self, pages:list):

        prev_btn:PaginatorButton = PaginatorButton("prev", None, PREV_EMOTE, ButtonStyle.blurple)
        next_btn:PaginatorButton = PaginatorButton("next", None, NEXT_EMOTE, ButtonStyle.blurple)

        buttons = []
        buttons.append(prev_btn)
        buttons.append(next_btn)


        super().__init__(
            pages,
            loop_pages=True, 
            disable_on_timeout=True, 
            show_indicator=False, 
            show_disabled=False, 
            use_default_buttons=False,
            custom_buttons=buttons
        )
