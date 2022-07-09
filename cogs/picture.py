from discord.ext import commands

from helpers import picture_helper

class PictureModule(commands.Cog):

    @commands.command(name="pfp", aliases=["profile_pic", "picture", "waifu"], description="Returns a random waifu.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def waifu(self, ctx:commands.Context):
        reply = await picture_helper.get_waifu_embed()

        await ctx.send(embed=reply)

def setup(bot):
    bot.add_cog(PictureModule())