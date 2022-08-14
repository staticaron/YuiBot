from discord.ext import commands
from discord import Member

from helpers import picture_helper

class PictureModule(commands.Cog):

    @commands.command(name="pfp", aliases=["profile_pic", "picture", "waifu"], description="Returns a random waifu.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def waifu(self, ctx:commands.Context):
        await ctx.trigger_typing()
        reply = await picture_helper.get_waifu_embed()

        await ctx.send(embed=reply)

    @commands.command(name="gif", aliases=["react"], description="Returns a cry/sob gif")
    async def cry(self, ctx:commands.Context, reaction:str, target:Member=None):
        await ctx.trigger_typing()
        reply = await picture_helper.get_reaction_embed(reaction, ctx.author, target)

        await ctx.send(embed=reply)

def setup(bot):
    bot.add_cog(PictureModule(bot))
