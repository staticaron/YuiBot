from discord.ext import commands

from helpers import general_helper, media_helper
from config import ERROR_COLOR


class MediaModule(commands.Cog):

    """Update the anime progress"""

    @commands.command(name="update_anime", aliases=["ua"], description="Sets the progress for the provided anime")
    async def update_anime(self, ctx: commands.Context, *inputs):

        await ctx.trigger_typing()

        ep = None
        anime = None

        try:
            ep = float(inputs[-1])
            anime = " ".join(inputs[:-1])
        except Exception as e:
            return await ctx.reply(embed=await general_helper.get_information_embed("Last parameter must be a decimal value representing the new score.", color=ERROR_COLOR))

        async def reply_callback():

            mediaID = data_elements[paginator.current_page].anilist_id

            return await media_helper.set_progress(str(ctx.author.id), mediaID, ep)

        data_inclusive_paginator = await general_helper.get_media_selection_paginator(anime, reply_callback)

        paginator = data_inclusive_paginator.paginator
        data_elements = data_inclusive_paginator.data_elements

        if data_inclusive_paginator.length() <= 0:
            await data_inclusive_paginator.get_error_embed()
        else:
            await paginator.send(ctx)

    """Update the manga progress"""

    @commands.command(name="update_manga", aliases=["um"], description="Sets the progress for the provided anime")
    async def update_manga(self, ctx: commands.Context, *inputs):

        await ctx.trigger_typing()

        ep = None
        anime = None

        try:
            ep = float(inputs[-1])
            anime = " ".join(inputs[:-1])
        except Exception as e:
            return await ctx.reply(embed=await general_helper.get_information_embed("Last parameter must be a decimal value representing the new score.", color=ERROR_COLOR))

        async def reply_callback():

            mediaID = data_elements[paginator.current_page].anilist_id

            return await media_helper.set_progress(str(ctx.author.id), mediaID, ep)

        data_inclusive_paginator = await general_helper.get_media_selection_paginator(anime, reply_callback, "MANGA")

        paginator = data_inclusive_paginator.paginator
        data_elements = data_inclusive_paginator.data_elements

        if data_inclusive_paginator.length() <= 0:
            await data_inclusive_paginator.get_error_embed()
        else:
            await paginator.send(ctx)

    """Rate Anime"""

    @commands.group(name="rate", description="Group Container of rate commands", case_insensitive=True)
    async def rate(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            return await ctx.reply("Please provide a valid subcommand. Try ```yui help rate```")

    @rate.command(name="anime", description="Rate anime", case_insensitive=True)
    async def rate_anime(self, ctx: commands.Context, *inputs):

        await ctx.trigger_typing()

        rating = None
        anime = None

        try:
            rating = float(inputs[-1])
            anime = " ".join(inputs[:-1])
        except Exception as e:
            return await ctx.reply(embed=await general_helper.get_information_embed("Last parameter must be a decimal value representing the new score.", color=ERROR_COLOR))

        async def selection_reply():
            anime_id = data_elements[paginator.current_page].anilist_id

            return await media_helper.rate_media(str(ctx.author.id), anime_id, rating)

        selection_result = await general_helper.get_media_selection_paginator(anime, selection_reply)

        paginator = selection_result.paginator
        data_elements = selection_result.data_elements

        if selection_result.length() <= 0:
            await ctx.reply(embed=await selection_result.get_error_embed())
        else:
            await paginator.send(ctx)

    @rate.command(name="manga", description="Rate manga", case_insensitive=True)
    async def rate_anime(self, ctx: commands.Context, *inputs):

        await ctx.trigger_typing()

        rating = None
        manga = None

        try:
            rating = float(inputs[-1])
            manga = " ".join(inputs[:-1])
        except Exception as e:
            return await ctx.reply(embed=await general_helper.get_information_embed("Last parameter must be a decimal value representing the new score.", color=ERROR_COLOR))

        async def selection_reply():
            manga_id = data_elements[paginator.current_page].anilist_id

            return await media_helper.rate_media(str(ctx.author.id), manga_id, rating)

        selection_result = await general_helper.get_media_selection_paginator(manga, selection_reply, "MANGA")

        paginator = selection_result.paginator
        data_elements = selection_result.data_elements

        if selection_result.length() <= 0:
            await ctx.reply(embed=await selection_result.get_error_embed())
        else:
            await paginator.send(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(MediaModule())
