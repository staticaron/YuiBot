from discord.ext import commands

from helpers import general_helper
import config


class UtilityModule(commands.Cog):
    @commands.command(name="hello", aliases=["hi", "hola", "konnichiwa", "sup", "ping"], description="Returns Bot's Latency")
    @general_helper.with_typing_ctx()
    async def latency(self, ctx: commands.Context):
        await ctx.reply(f"Hello **{ctx.author.name}** {config.YUI_SHY_EMOTE} - took **{round(ctx.bot.latency * 1000, 2)} ms**")

    @commands.command(name="invite", description="Returns an invite link for the bot.")
    @general_helper.with_typing_ctx()
    async def invite(self, ctx: commands.Context):
        await ctx.send(embed=await general_helper.get_information_embed(title="Invite Me!", description="[Click Here]({}) to invite me to your server.".format(config.INVITE), thumbnail_link=ctx.bot.user.avatar.url))

    @commands.command(name="support", aliases=["server"], description="Sends Link to join the official support server.")
    @general_helper.with_typing_ctx()
    async def support(self, ctx: commands.Context):
        await ctx.send(embed=await general_helper.get_information_embed(title="Support Server!", description="[Click Here]({}) to join the support server.".format(config.SUPPORT_SERVER_LINK), thumbnail_link=ctx.bot.user.avatar.url))


def setup(bot: commands.Bot):
    bot.add_cog(UtilityModule())
