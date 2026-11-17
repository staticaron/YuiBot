from discord import Embed
from discord.ext import commands

from config import ERROR_COLOR
from helpers import general_helper, media_helper, theme_scrapper
from views.scroller import Scroller


class MediaModule(commands.Cog):
    """Update the anime progress"""

    @commands.command(
        name="update_anime",
        aliases=["ua"],
        description="Sets the progress for the provided anime",
    )
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def update_anime(self, ctx: commands.Context, *inputs):
        ep = None
        anime = None

        try:
            anime = " ".join(inputs[:-1])
            ep = int(inputs[-1])
        except Exception:  # noqa: BLE001
            ep = -1
            anime = " ".join(inputs)

        async def reply_callback() -> Embed:
            mediaID = data_elements[paginator.current_page].anilist_id

            return await media_helper.set_progress(str(ctx.author.id), mediaID, ep)

        data_inclusive_paginator = await general_helper.get_media_selection_paginator(
            anime, reply_callback
        )

        paginator = data_inclusive_paginator.paginator
        data_elements = data_inclusive_paginator.data_elements

        if data_inclusive_paginator.length() <= 0:
            await data_inclusive_paginator.get_error_embed()
        else:
            await paginator.send(ctx)

    """Update the manga progress"""

    @commands.command(
        name="update_manga",
        aliases=["um"],
        description="Sets the progress for the provided anime",
    )
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def update_manga(self, ctx: commands.Context, *inputs):
        ep = None
        manga = None

        try:
            manga = " ".join(inputs[:-1])
            ep = int(inputs[-1])
        except Exception:  # noqa: BLE001
            ep = -1
            manga = " ".join(inputs)

        async def reply_callback() -> Embed:
            mediaID = data_elements[paginator.current_page].anilist_id
            return await media_helper.set_progress(str(ctx.author.id), mediaID, ep)

        data_inclusive_paginator = await general_helper.get_media_selection_paginator(
            manga, reply_callback, "MANGA"
        )

        paginator = data_inclusive_paginator.paginator
        data_elements = data_inclusive_paginator.data_elements

        if data_inclusive_paginator.length() <= 0:
            await data_inclusive_paginator.get_error_embed()
        else:
            await paginator.send(ctx)

    """Rate Anime"""

    @commands.group(
        name="rate",
        description="Group Container of rate commands",
        case_insensitive=True,
    )
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    async def rate(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            return await ctx.reply(
                "Please provide a valid subcommand. Try ```yui help rate```"
            )

    @rate.command(name="anime", description="Rate anime", case_insensitive=True)
    @general_helper.with_typing_ctx()
    async def rate_anime(self, ctx: commands.Context, *inputs):
        rating = None
        anime = None

        try:
            rating = float(inputs[-1])
            anime = " ".join(inputs[:-1])
        except Exception:  # noqa: BLE001
            return await ctx.reply(
                embed=await general_helper.get_information_embed(
                    "Last parameter must be a decimal value representing the new score.",
                    color=ERROR_COLOR,
                )
            )

        async def selection_reply() -> Embed:
            anime_id = data_elements[paginator.current_page].anilist_id
            return await media_helper.rate_media(str(ctx.author.id), anime_id, rating)

        selection_result = await general_helper.get_media_selection_paginator(
            anime, selection_reply
        )

        paginator = selection_result.paginator
        data_elements = selection_result.data_elements

        if selection_result.length() <= 0:
            await ctx.reply(embed=await selection_result.get_error_embed())
        else:
            await paginator.send(ctx)

    @rate.command(name="manga", description="Rate manga", case_insensitive=True)
    @general_helper.with_typing_ctx()
    async def rate_manga(self, ctx: commands.Context, *inputs):
        rating = None
        manga = None

        try:
            rating = float(inputs[-1])
            manga = " ".join(inputs[:-1])
        except Exception:  # noqa: BLE001
            return await ctx.reply(
                embed=await general_helper.get_information_embed(
                    "Last parameter must be a decimal value representing the new score.",
                    color=ERROR_COLOR,
                )
            )

        async def selection_reply() -> Embed:
            manga_id = data_elements[paginator.current_page].anilist_id
            return await media_helper.rate_media(str(ctx.author.id), manga_id, rating)

        selection_result = await general_helper.get_media_selection_paginator(
            manga, selection_reply, "MANGA"
        )

        paginator = selection_result.paginator
        data_elements = selection_result.data_elements

        if selection_result.length() <= 0:
            await ctx.reply(embed=await selection_result.get_error_embed())
        else:
            await paginator.send(ctx)

    """Get Anime Op/Ed"""

    @commands.command(
        name="theme",
        aliases=["song", "op", "ed", "music"],
        description="Returns the links to opening and ending music of the provided anime",
    )
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def themes(self, ctx: commands.Context, *inputs):
        anime = " ".join(inputs)

        async def reply_callback() -> Scroller:
            selected_id = data_elements[paginator.current_page].mal_id
            return await theme_scrapper.get_themes_embed(selected_id)

        anime_selector = await general_helper.get_media_selection_paginator(
            anime, reply_callback
        )

        paginator = anime_selector.paginator
        data_elements = anime_selector.data_elements

        if anime_selector.length() <= 0:
            error_embed = await anime_selector.get_error_embed()
            await ctx.reply(embed=error_embed)
        else:
            await paginator.send(ctx)

    """Anime watch order"""

    @commands.command(
        name="watch_order",
        aliases=["wo", "order"],
        description="Returns the watch order of the selected anime",
    )
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def watch_order(self, ctx: commands.Context, *inputs):
        anime = " ".join(inputs)

        async def reply_callback() -> Scroller:
            mal_id = data_elements[paginator.current_page].mal_id
            return await media_helper.get_watch_order_embd(mal_id, anime)

        selector = await general_helper.get_media_selection_paginator(
            anime, reply_callback
        )

        paginator = selector.paginator
        data_elements = selector.data_elements

        if selector.length() <= 0:
            await ctx.reply(embed=await selector.get_error_embed())
        else:
            await paginator.send(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(MediaModule())
