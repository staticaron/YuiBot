from discord import ButtonStyle
from discord.ext import pages
from discord.ext.pages import PaginatorButton

from config import PREV_EMOTE, NEXT_EMOTE, FIRST_EMOTE, LAST_EMOTE

class Scroller(pages.Paginator):

    def __init__(self, pages:list, show_all_btns:bool = False):

        prev_btn:PaginatorButton = PaginatorButton("prev", None, PREV_EMOTE, ButtonStyle.blurple)
        next_btn:PaginatorButton = PaginatorButton("next", None, NEXT_EMOTE, ButtonStyle.blurple)
        first_btn:PaginatorButton = PaginatorButton("first", None, FIRST_EMOTE, ButtonStyle.blurple)
        last_btn:PaginatorButton = PaginatorButton("last", None, LAST_EMOTE, ButtonStyle.blurple)

        buttons = []

        if show_all_btns:
            buttons.append(first_btn)

        buttons.append(prev_btn)
        buttons.append(next_btn)

        if show_all_btns:
            buttons.append(last_btn)


        super().__init__(
            pages,
            loop_pages=True, 
            disable_on_timeout=True, 
            show_indicator=False, 
            show_disabled=True,
            use_default_buttons=False,
            custom_buttons=buttons
        )
