from discord import Member
from discord.ext import commands

from helpers import general_helper, lists_helper
import config

class ListsModule(commands.Cog):

    """View Favorite Anime"""

    @commands.command(name="favanime", aliases=["fa", "favorite_anime"], description="Returns your favorite anime list")
    @commands.check(general_helper.validate_user)
    async def fav_anime_list(self, ctx:commands.Context, target:Member=None):

        await ctx.trigger_typing()

        target = (ctx.author if target is None else target)

        paginator = await lists_helper.get_fav_paginator(target, "ANIME")

        if paginator is not None:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )


    """View Favorite Manga"""

    @commands.command(name="favmanga", aliases=["fm", "favorite_manga"], description="Returns your favorite manga list")
    @commands.check(general_helper.validate_user)
    async def fav_manga_list(self, ctx:commands.Context, target:Member=None):

        await ctx.trigger_typing()

        target = (ctx.author if target is None else target)

        paginator = await lists_helper.get_fav_paginator(target, "MANGA")

        if paginator is not None:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )

    """Add Anime to Lists/Fav"""

    @commands.command(name="addanime", aliases=["aa"], case_insensitive=True, description="Adds anime to your mentioned list")
    @commands.check(general_helper.validate_user)
    async def addanime(self,ctx:commands.Context, list_name:str, *anime):

        await ctx.trigger_typing()

        # check for valid list
        if list_name.lower() not in lists_helper.all_lists:
            return await ctx.reply(embed=await general_helper.get_information_embed(
                title="Hold It",
                description="The following error occurred : ```INVALID LIST NAME``` Provide one of these list names : Planning, Dropped, Watching, Completed",
                color=config.ERROR_COLOR
            )
        )

        anime = " ".join(anime)

        async def reply_callback():

            mediaId = ids[paginator.current_page]

            #modify the ptw list
            return await lists_helper.add_to_list(list_name, mediaId, ctx.author)
            
        response = await general_helper.get_media_selection_paginator(media_name=anime, select_callback=reply_callback)

        paginator = response.paginator
        ids = [str(anime.media_id) for anime in response.media]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

    """Add Manga to Lists"""

    @commands.command(name="addmanga", aliases=["am"], case_insensitive=True, description="Adds anime to your mentioned list")
    @commands.check(general_helper.validate_user)
    async def addmanga(self,ctx:commands.Context, list_name:str, *manga):

        await ctx.trigger_typing()

        # check for valid list
        if list_name.lower() not in lists_helper.all_lists:
            return await ctx.reply(embed=await general_helper.get_information_embed(
                title="Hold It",
                description="The following error occurred : ```INVALID LIST NAME``` Provide one of these list names : Planning, Dropped, Watching, Completed",
                color=config.ERROR_COLOR
            )
        )

        manga = " ".join(manga)

        async def reply_callback():

            mediaId = ids[paginator.current_page]

            #modify the ptw list
            return await lists_helper.add_to_list(list_name, mediaId, ctx.author, "MANGA")
            
        response = await general_helper.get_media_selection_paginator(media_name=manga, select_callback=reply_callback, media_type="MANGA")

        paginator = response.paginator
        ids = [str(anime.media_id) for anime in response.media]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

    """View Planning Lists"""

    @commands.command(name="ptw", aliases=["planning"], case_insensitive=True, description="Returns the planning list of the user/member")
    @commands.check(general_helper.validate_user)
    async def planning_list(self, ctx:commands.Context, user:Member=None):
        
        await ctx.trigger_typing()

        user = (user if user is not None else ctx.author)

        reply = await lists_helper.get_list_paginator(user, "PLANNING")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )
        
    """View Watching Lists"""
    
    @commands.command(name="wtc", aliases=["watching"], case_insensitive=True, description="Returns the watching list of the user/member")
    @commands.check(general_helper.validate_user)
    async def watching_list(self, ctx:commands.Context, user:Member=None):

        await ctx.trigger_typing()
           
        user = (user if user is not None else ctx.author)

        reply = await lists_helper.get_list_paginator(user, "CURRENT")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )

    """View Completed Lists"""

    @commands.command(name="comp", aliases=["completed"], case_insensitive=True, description="Returns the completed list of the user/member")
    @commands.check(general_helper.validate_user)
    async def completed_list(self, ctx:commands.Context, user:Member=None):

        await ctx.trigger_typing()
           
        user = (user if user is not None else ctx.author)

        reply = await lists_helper.get_list_paginator(user, "COMPLETED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )

    """View Dropped Lists"""

    @commands.command(name="drp", aliases=["dropped"], case_insensitive=True, description="Returns the dropped list of the user/member")
    @commands.check(general_helper.validate_user)
    async def dropped_list(self, ctx:commands.Context, user:Member=None):
        
        await ctx.trigger_typing()
          
        user = (user if user is not None else ctx.author)

        reply = await lists_helper.get_list_paginator(user, "DROPPED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )

    """View Paused Lists"""

    @commands.command(name="psd", aliases=["paused"], case_insensitive=True, description="Returns the paused list of the user/member")
    @commands.check(general_helper.validate_user)
    async def paused_list(self, ctx:commands.Context, user:Member=None):
        
        await ctx.trigger_typing()
          
        user = (user if user is not None else ctx.author)

        reply = await lists_helper.get_list_paginator(user, "PAUSED")

        if reply is not None:
            await reply.send(ctx)
        else:
            await ctx.reply(embed=
                await general_helper.get_information_embed(
                    title="Hold It!",
                    description="No Media entries were found in this list.",
                    color=config.INFO_COLOR
                )
            )

def setup(bot:commands.Bot):
    bot.add_cog(ListsModule())