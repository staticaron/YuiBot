from discord.ext import commands

import config
from helpers import general_helper


class UtilityModule(commands.Cog):
    @commands.command(
        name="hello",
        aliases=["hi", "hola", "konnichiwa", "sup", "ping"],
        description="Returns Bot's Latency",
    )
    @general_helper.with_typing_ctx()
    async def latency(self, ctx: commands.Context):
        await ctx.reply(
            f"Hello **{ctx.author.name}** {config.YUI_SHY_EMOTE} - took **{round(ctx.bot.latency * 1000, 2)} ms**"
        )

    @commands.command(name="invite", description="Returns an invite link for the bot.")
    @general_helper.with_typing_ctx()
    async def invite(self, ctx: commands.Context):
        await ctx.send(
            embed=await general_helper.get_information_embed(
                title="Invite Me!",
                description=f"[Click Here]({config.INVITE}) to invite me to your server.",
                thumbnail_link=ctx.bot.user.avatar.url,
            )
        )

    @commands.command(
        name="support",
        aliases=["server"],
        description="Sends Link to join the official support server.",
    )
    @general_helper.with_typing_ctx()
    async def support(self, ctx: commands.Context):
        await ctx.send(
            embed=await general_helper.get_information_embed(
                title="Support Server!",
                description=f"[Click Here]({config.SUPPORT_SERVER_LINK}) to join the support server.",
                thumbnail_link=ctx.bot.user.avatar.url,
            )
        )


def setup(bot: commands.Bot):
    bot.add_cog(UtilityModule())
