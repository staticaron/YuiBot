from discord.ext import commands
from discord.ui import Button

from helpers import general_helper, lists_helper
import config

class ListsModule(commands.Cog):

    @commands.command(name="add", case_insensitive=True, description="Adds anime to your mentioned list")
    @commands.check(general_helper.validate_user)
    async def add(self,ctx:commands.Context, list_name:str, *anime):

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
            
        response = await general_helper.get_anime_selection_paginator(anime=anime, select_callback=reply_callback)

        paginator = response.paginator
        ids = [str(anime.media_id) for anime in response.anime]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())
        

def setup(bot:commands.Bot):
    bot.add_cog(ListsModule())