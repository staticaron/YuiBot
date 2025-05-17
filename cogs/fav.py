from discord.ext import commands

from helpers import lists_helper, general_helper


class FavModule(commands.Cog):
    @commands.group(name="togglefav", aliases=["tf"], description="Toggles the media/character fav", case_insensitive=True)
    @commands.check(general_helper.validate_user)
    async def toggle_fav(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Provide a valid subcommand")

    @toggle_fav.command(name="anime", aliases=["a"], description="Adds/Removes anime to favs", case_insensitive=True)
    @general_helper.with_typing_ctx()
    async def fav_anime(self, ctx: commands.Context, *inputs):
        await ctx.trigger_typing()

        anime = " ".join(inputs)

        async def reply_callback():
            mediaId = ids[paginator.current_page]

            return await lists_helper.add_to_fav(mediaId, ctx.author)

        response = await general_helper.get_media_selection_paginator(media_name=anime, select_callback=reply_callback)

        paginator = response.paginator
        ids = [str(anime.anilist_id) for anime in response.data_elements]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

    @toggle_fav.command(name="manga", aliases=["m"], description="Adds/Removes manga to favs", case_insensitive=True)
    @general_helper.with_typing_ctx()
    async def fav_manga(self, ctx: commands.Context, *inputs):
        await ctx.trigger_typing()

        manga = " ".join(inputs)

        async def reply_callback():
            mediaId = ids[paginator.current_page]

            return await lists_helper.add_to_fav(mediaId, ctx.author, media_type="MANGA")

        response = await general_helper.get_media_selection_paginator(media_name=manga, select_callback=reply_callback, media_type="MANGA")

        paginator = response.paginator
        ids = [str(manga.anilist_id) for manga in response.data_elements]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

    @toggle_fav.command(name="character", aliases=["c", "char"], description="Adds/Removes characters to favs", case_insensitive=True)
    @general_helper.with_typing_ctx()
    async def fav_char(self, ctx: commands.Context, *inputs):
        await ctx.trigger_typing()

        char = " ".join(inputs)

        async def reply_callback():
            mediaId = ids[paginator.current_page]

            return await lists_helper.add_to_fav(mediaId, ctx.author, "CHARACTER")

        response = await general_helper.get_character_selection_paginator(character_name=char, select_callback=reply_callback)

        paginator = response.paginator
        ids = [str(char.anilist_id) for char in response.data_elements]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())


def setup(bot: commands.Bot):
    bot.add_cog(FavModule())
