from discord.ext import commands
from discord import Embed

from views.scroller import Scroller
from helpers import general_helper
import config


class FillerModule(commands.Cog):
    async def search_filler(self, query):
        ret = {}

        index = config.FILLER_DATA["info"]

        keys = list(index.keys())

        for i in range(len(keys)):
            matching_name = True

            for j in query.split():
                if j.lower() not in keys[i]:
                    matching_name = False
                    break

            if matching_name:
                ret[keys[i]] = index[keys[i]]

        return ret

    async def parse_filler(self, anime_match: dict) -> list:
        embds = []

        if len(anime_match.items()) <= 0:
            return [Embed(title="No Filler Information was found!", color=config.NORMAL_COLOR)]

        # True if at least one filler data item was found.
        filler_found: bool = False

        for name, id in anime_match.items():
            try:
                data = config.FILLER_DATA["data"][id]
            except KeyError as e:
                if filler_found is False:
                    embds.append(Embed(title="No Filler Information was found!", color=config.NORMAL_COLOR))
                    continue
                continue
            else:
                if filler_found is False:
                    filler_found = True
                    embds.clear()

            embd = Embed(title="{name}'s Filler Episodes".format(name=name), color=config.NORMAL_COLOR)

            try:
                embd.add_field(name="Anime Canon Episodes", value="```{}```".format(data["anime_canon"]), inline=False)

                embd.add_field(name="Manga Canon Episodes", value="```{}```".format(data["manga_canon"]), inline=False)

                embd.add_field(name="Mixed Episodes", value="```{}```".format(data["mixed_ep"]), inline=False)

                embd.add_field(name="Filler Episodes", value="```{}```".format(data["filler_ep"]), inline=False)
            except Exception as e:
                print(name)

            embds.append(embd)

        return embds

    @commands.command(name="filler", description="Returns a list of all the recorded filler episodes of the anime")
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def filler(self, ctx: commands.Context, *anime):
        anime = " ".join(anime)

        print("Anime name is " + anime)

        anime_match = await self.search_filler(anime)

        print(anime_match)

        embds = await self.parse_filler(anime_match)

        if len(embds) == 1:
            await ctx.send(embed=embds[0])
        else:
            scroller = Scroller(embed_pages=embds, show_all_btns=True)
            await scroller.send(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(FillerModule())
