from discord.ext import commands
from discord.ext import pages
import requests

from helpers import general_helper, non_media_helper

class Non_Media_Module(commands.Cog):
    
    @commands.group(name="character", description="Commands related to managing characters in your anilist")
    async def character(self, ctx:commands.Context):
        if ctx.subcommand_passed ==  None:
            await ctx.reply("Please provide valid subcommand. Try ```yui help character```")

    @character.command(name="fav", description="Returns your favorite characters or adds the provided character to favorites", case_insensitive=False)
    async def favorite(self, ctx:commands.Context, *character):

        await ctx.trigger_typing()

        if len(character) <= 0:
            # return a list of favorite characters
            return 

        character = " ".join(character)

        async def character_selection_callback():
            character_id = ids[response.paginator.current_page]

            return await non_media_helper.add_fav_character(ctx.author, int(character_id))

        response = await general_helper.get_character_selection_paginator(character, character_selection_callback)

        paginator:pages.Paginator = response.paginator
        ids = [str(data_element.anilist_id) for data_element in response.data_elements]

        if response.length() > 0:
            await paginator.send(ctx)
        else:
            await ctx.reply(embed=await response.get_error_embed())

def setup(bot:commands.Bot):
    bot.add_cog(Non_Media_Module())