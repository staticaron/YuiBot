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

        async def select_callback(self):

            mediaId = ids[paginator.current_page]

            #modify the ptw list
            reply = await lists_helper.add_to_list(list_name, mediaId, ctx.author)

            paginator.clear_items()

            await ctx.reply(embed=reply)

            
        response = await general_helper.get_anime_selection_paginator(anime=anime, select_callback=select_callback)

        paginator = response.paginator
        ids = [str(anime.media_id) for anime in response.anime]

        await paginator.send(ctx)

def setup(bot:commands.Bot):
    bot.add_cog(ListsModule())