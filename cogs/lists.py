from discord import Member
from discord.ext import commands

from helpers import general_helper, lists_helper
import config


class ListsModule(commands.Cog):
    """

    ANIME

    """

    @commands.group(name="anime", description="Commands about your anime lists")
    @commands.check(general_helper.validate_user)
    async def anime_group(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide a valid subcommand.")

    """View Favorite Anime"""

    @anime_group.command(name="fav", aliases=["favorite"], description="Returns your favorite anime list")
    @commands.check(general_helper.validate_user)
    @general_helper.with_typing_ctx()
    async def fav_anime_list(self, ctx: commands.Context, target: Member = None):
        target = ctx.author if target is None else target

        paginator = await lists_helper.get_fav_paginator(target, "ANIME")

        if paginator is not None:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """Add Anime to Lists"""

    @commands.command(name="addanime", aliases=["aa"], case_insensitive=True, description="Adds anime to your mentioned list")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def addanime(self, ctx: commands.Context, list_name: str, *anime):
        # check for valid list
        if list_name.lower() not in lists_helper.all_lists:
            return await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It", description="The following error occurred : ```INVALID LIST NAME``` Provide one of these list names : Planning, Dropped, Watching, Completed", color=config.ERROR_COLOR))

        anime = " ".join(anime)

        async def reply_callback():
            mediaId = ids[paginator.current_page]

            # modify the ptw list
            return await lists_helper.add_to_list(list_name, mediaId, ctx.author)

        response = await general_helper.get_media_selection_paginator(media_name=anime, select_callback=reply_callback)

        paginator = response.paginator
        ids = [str(anime.anilist_id) for anime in response.data_elements]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

    """View Planning Lists"""

    @anime_group.command(name="ptw", aliases=["planning"], case_insensitive=True, description="Returns the planning list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def anime_planning_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "ANIME", "PLANNING")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Watching Lists"""

    @anime_group.command(name="wtc", aliases=["watching"], case_insensitive=True, description="Returns the watching list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def anime_watching_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "ANIME", "CURRENT")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Completed Lists"""

    @anime_group.command(name="comp", aliases=["completed"], case_insensitive=True, description="Returns the completed list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def anime_completed_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "ANIME", "COMPLETED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Dropped Lists"""

    @anime_group.command(name="drp", aliases=["dropped"], case_insensitive=True, description="Returns the dropped list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def anime_dropped_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "ANIME", "DROPPED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Paused Lists"""

    @anime_group.command(name="psd", aliases=["paused"], case_insensitive=True, description="Returns the paused list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def anime_paused_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "ANIME", "PAUSED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """
    
    MANGA
    
    """

    @commands.group(name="manga", description="Commands about your manga lists")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    async def manga_group(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide a valid subcommand.")

    """View Favorite Manga"""

    @manga_group.command(name="fav", aliases=["favorite"], description="Returns your favorite manga list")
    @commands.check(general_helper.validate_user)
    @general_helper.with_typing_ctx()
    async def fav_manga_list(self, ctx: commands.Context, target: Member = None):
        target = ctx.author if target is None else target

        paginator = await lists_helper.get_fav_paginator(target, "MANGA")

        if paginator is not None:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """Add Manga to Lists"""

    @commands.command(name="addmanga", aliases=["am"], case_insensitive=True, description="Adds anime to your mentioned list")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def addmanga(self, ctx: commands.Context, list_name: str, *manga):
        # check for valid list
        if list_name.lower() not in lists_helper.all_lists:
            return await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It", description="The following error occurred : ```INVALID LIST NAME``` Provide one of these list names : Planning, Dropped, Watching, Completed", color=config.ERROR_COLOR))

        manga = " ".join(manga)

        async def reply_callback():
            mediaId = ids[paginator.current_page]

            # modify the ptw list
            return await lists_helper.add_to_list(list_name, mediaId, ctx.author, "MANGA")

        response = await general_helper.get_media_selection_paginator(media_name=manga, select_callback=reply_callback, media_type="MANGA")

        paginator = response.paginator
        ids = [str(anime.anilist_id) for anime in response.data_elements]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

    """View Planning Lists"""

    @manga_group.command(name="ptr", aliases=["planning"], case_insensitive=True, description="Returns the planning list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def manga_planning_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "MANGA", "PLANNING")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Watching Lists"""

    @manga_group.command(name="rd", aliases=["reading"], case_insensitive=True, description="Returns the watching list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def manga_reading_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "MANGA", "CURRENT")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Completed Lists"""

    @manga_group.command(name="comp", aliases=["completed"], case_insensitive=True, description="Returns the completed list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def manga_completed_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "MANGA", "COMPLETED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Dropped Lists"""

    @manga_group.command(name="drp", aliases=["dropped"], case_insensitive=True, description="Returns the dropped list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def manga_dropped_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "MANGA", "DROPPED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))

    """View Paused Lists"""

    @manga_group.command(name="psd", aliases=["paused"], case_insensitive=True, description="Returns the paused list of the user/member")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def manga_paused_list(self, ctx: commands.Context, user: Member = None):
        user = user if user is not None else ctx.author

        reply = await lists_helper.get_list_paginator(user, "MANGA", "PAUSED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=await general_helper.get_information_embed(title="Hold It!", description="No Media entries were found in this list.", color=config.INFO_COLOR))


def setup(bot: commands.Bot):
    bot.add_cog(ListsModule())
