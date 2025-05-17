from discord.ext import commands

from helpers import general_helper, non_media_helper


class Non_Media_Module(commands.Cog):
    @commands.group(name="character", aliases=["char"], description="Commands related to managing characters in your anilist", case_insensitive=True)
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def character(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide valid subcommand. Try ```yui help character```")

    @character.command(name="fav", description="Returns your favorite characters if no param is provided else adds the provided character to favorites", case_insensitive=True)
    @general_helper.with_typing_ctx()
    async def favorite(self, ctx: commands.Context):
        fav_scroller = await non_media_helper.get_fav_character_scroller(ctx.author)

        return await fav_scroller.send(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(Non_Media_Module())
