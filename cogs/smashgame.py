from discord.ext import commands
from discord import Embed
import asyncio

from views.smash_view import SmashView
from managers import mongo_manager
from helpers import picture_helper
import config

class SmashGame(commands.Cog):

    @commands.command(name="smashgame", aliases=["smash"], description="Starts a Smash or Pass game session")
    @commands.max_concurrency(1, per=commands.BucketType.channel)
    async def smashgame(self, ctx:commands.Context, count:int=10):

        WAIT_TIME = 10

        count = (20 if count > 20 else count and 0 if count < 0 else count)

        for i in range(count):

            url = await picture_helper.fetch_waifu_api()

            embd = Embed(title="Smash?", color=config.NORMAL_COLOR)
            embd.set_image(url=url)

            view = SmashView(message=ctx.message, timeout=WAIT_TIME)

            await ctx.send(embed=embd, view=view)

            await asyncio.sleep(WAIT_TIME)

        await mongo_manager.manager.update_smash_leaderboard()
        await ctx.send("Smash or Pass session ended! Thanks for playing.")

def setup(bot:commands.Bot):
    bot.add_cog(SmashGame())