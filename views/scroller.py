from discord import ButtonStyle
from discord.ext import pages
from discord.ext.pages import PaginatorButton

from config import PREV_EMOTE, NEXT_EMOTE, FIRST_EMOTE, LAST_EMOTE


class Scroller(pages.Paginator):

    def __init__(self, embed_pages: list, show_all_btns: bool = False):

        prev_btn: PaginatorButton = PaginatorButton(
            "prev", None, PREV_EMOTE, ButtonStyle.gray)
        next_btn: PaginatorButton = PaginatorButton(
            "next", None, NEXT_EMOTE, ButtonStyle.gray)
        first_btn: PaginatorButton = PaginatorButton(
            "first", None, FIRST_EMOTE, ButtonStyle.gray)
        last_btn: PaginatorButton = PaginatorButton(
            "last", None, LAST_EMOTE, ButtonStyle.gray)

        buttons = []

        if show_all_btns:
            buttons.append(first_btn)

        buttons.append(prev_btn)
        buttons.append(next_btn)

        if show_all_btns:
            buttons.append(last_btn)

        for index in range(len(embed_pages)):
            embed_pages[index].set_footer(text=f"Page {index+1} of {len(embed_pages)}")

        super().__init__(
            embed_pages,
            loop_pages=True,
            disable_on_timeout=True,
            show_indicator=False,
            show_disabled=True,
            use_default_buttons=False,
            custom_buttons=buttons,
            timeout=30
        )
