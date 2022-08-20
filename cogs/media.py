from discord.ext import commands
from discord import Interaction

from helpers import general_helper, media_helper


class MediaModule(commands.Cog):

    """Update the anime progress"""

    @commands.command(name="update_anime", aliases=["ua"], description="Sets the progress for the provided anime")
    async def update_anime(self, ctx: commands.Context, *anime_episode):

        await ctx.trigger_typing()

        ep = anime_episode[-1]
        anime = " ".join(anime_episode[:-1])

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
    async def update_manga(self, ctx: commands.Context, *anime_episode):

        await ctx.trigger_typing()

        ep = anime_episode[-1]
        anime = " ".join(anime_episode[:-1])

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
    async def rate_anime(self, ctx: commands.Context, *anime):

        await ctx.trigger_typing()

        anime = " ".join(anime)

        async def selection_reply():
            anime_id = data_elements[paginator.current_page].anilist_id

        selection_result = await general_helper.get_media_selection_paginator(anime, selection_reply)

        paginator = selection_result.paginator
        data_elements = selection_result.data_elements

        if selection_result.length() <= 0:
            await ctx.reply(embed=selection_result.get_error_embed())
        else:
            await paginator.send(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(MediaModule())
