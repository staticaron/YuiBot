from discord.ext import commands
from discord import Embed

from helpers import general_helper
import config


class HelpCommand(commands.Cog):

    help_embed: Embed = None
    bot: commands.Bot = None

    modules = {
        "login": "Login and Logout Instructions",
        "detect": "Detect anime from images and gif",
        "info": "Get Information about Anime/Manga/Character/Studio , watch order, filler episodes data, anime suggestions",
        "media": "Update episode count, rate shows/manga, get opening and endings",
        "list": "To fetch or modify your lists",
        "misc": "Misc. command that don't fall in any category. Gifs, Quotes, Invite links and more",
        "user": "Follow/unfollow users, get theirs stats and more."
    }

    commands_per_module = {
        "login": ["login", "logout"],
        "detect": ["detect_anime"],
        "info": ["find", "watch_order", "filler", "suggest"],
        "list": ["addanime", "addmanga", "anime", "manga"],
        "media": ["update_anime", "update_manga", "rate", "theme"],
        "misc": ["gif", "pfp", "quote", "ping", "invite"],
        "user": ["follow", "unfollow", "info", "animestats", "mangastats"]
    }

    helps = {
        "login login": "Links you Anilist Account to the bot. ```yui login\nyui register```",
        "login logout": "Removes your anilist Account from the bot. ```yui logout```",
        "detect detect_anime": "Detects the anime present in the provided media. ```yui detect_anime <link>\nyui da <link>```",
        "user follow": "Follow any discord user who is registered with the bot by pinging them. ```yui follow @bestGuy```",
        "user unfollow": "Unfollow any discord user who is registered with the bot by pinging them. ```yui unfollow @OmegaWeeb```",
        "user info": "Returns your or someones else's profile data ```yui info\nyui info @DeltaWeeb```",
        "user animestats": "Returns the anime stats of any user. ```yui animestats\nyui animestats @BetaWeeb```",
        "user mangastats": "Returns the manga stats of any user. ```yui mangastats\nyui mangastats @AlphaWeeb```",
        "info find": "Fetches the anime/manga/character/studio details. ```yui find anime <anime_name / manga_name / character_name / studio_name>\nyui find anime k-on\nyui find manga Kimi to Picopico\nyui search character futaba igarashi\nyui search studio a-1 pictures\nyui find topanime <genre>\nyui search topmanga romance action```",
        "info watch_order": "Returns the watch order of the provided anime. ```yui watch_order <anime_name>\n\nyui watch_order pokemon\nyui wo haikyu```",
        "info filler": "Returns the filler episodes data of the provided anime. ```yui filler <anime_name>\n\nyui filler haikyu```",
        "info suggest": "Returns a list of recommendations based on the provided anime. ```yui suggest <anime_name>\n\nyui suggest konosuba```",
        "list addanime": "Adds the provided anime to the provided list. ```yui addanime <list_name> <anime_name>\n\nyui addanime ptw your lie in april\nyui aa dropped pokemon journeys```",
        "list addmanga": "Adds the provided manga to the provided list. ```yui addmanga <list_name> <manga_name>\n\nyui addmanga comp komi can't communicate\nyui am ptr kaguya sama```",
        "list anime": "Returns the provided list from your or any other anilist account. ```yui anime <list_name>\n\nyui anime dropped\nyui anime planning\nyui anime watching @user```",
        "list manga": "Returns the provided list from your or any other anilist account. ```yui manga <list_name>\n\nyui manga dropped\nyui manga reading\nyui manga completed @user```",
        "media update_anime": "Updates the progress/episode count of the provided anime. ```yui update_anime <anime_name> <new_progress>\n\nyui update_anime toradora 5\nyui ua kanokari 8```",
        "media update_manga": "Updates the progress/episode count of the provided manga. ```yui update_manga <manga_name> <new_progress>\n\nyui update_manga chainsaw man 5\nyui um k-on 8```",
        "media rate": "Rates a particular anime/manga ```yui rate anime <anime_name> <new_score>\n\nyui rate anime haikyu 100\nyui rate manga berserk 80```",
        "media theme": "Returns the opening and endings of the provided anime with their links. ```yui theme <anime_name>\n\nyui theme shikimori is not just a cutie\nyui op and you thought there was never a girl online```",
        "misc gif": "Returns a reaction gif on supported type. ```yui gif happy\nyui gif bonk\nyui gif wave",
        "misc pfp": "Returns a random waifu image. Can be used for getting random profile pictures. ```yui pfp```",
        "misc quote": "Returns a random anime quote ```yui quote```",
        "misc invite": "Sends the invite link of the bot",
        "misc ping": "Returns the bot's current latency. ```yui hi\nyui ping```"
    }

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="help", description="Get help with bot commands", case_insensitive=True)
    async def help(self, ctx: commands.Context, *inputs):

        inputs = [x.lower() for x in inputs]

        if len(inputs) <= 0:
            if self.help_embed is None:
                self.help_embed = await general_helper.get_information_embed(
                    title="Help Menu", description="Use `yui help <module>` and pass any one module from the following list. \n\nExample : yui help **media** \n\n **Modules** : ", thumbnail_link=ctx.bot.user.avatar.url)

                for module, description in self.modules.items():
                    self.help_embed.add_field(
                        name=module,
                        value=description,
                        inline=False
                    )
            await ctx.send(embed=self.help_embed)

        if len(inputs) == 1:
            module = inputs[0]

            all_modules = list(self.modules.keys())

            if module not in all_modules:
                return await ctx.reply(embed=await general_helper.get_information_embed(title="Module Not Found!", description="Pick a module from the list using **yui help** command.", color=config.ERROR_COLOR))

            embd = await general_helper.get_information_embed(title=f"{module.capitalize()}'s Help", description=f"Use `yui help {module} <command>` and pass one command from the following list. \n\n Example : yui help {module} **{self.commands_per_module[module][0]}** \n\n **__Commands__** : \n\n", thumbnail_link=ctx.bot.user.avatar.url)

            for i in self.commands_per_module[module]:
                embd.description += f"{config.BULLET_EMOTE} **{i}** : {self.bot.get_command(i).description} \n"

            await ctx.send(embed=embd)

        if len(inputs) >= 2:
            command = " ".join([x.lower() for x in inputs[:2]])

            if command not in list(self.helps.keys()):
                return await ctx.reply(embed=await general_helper.get_information_embed(title="Command Not Found!", description=f"Pick a command from the list using **yui help {command.split()[0]}** command.", color=config.ERROR_COLOR))

            embd = await general_helper.get_information_embed(title=f"{command}'s Help", description=self.helps[command], thumbnail_link=self.bot.user.avatar.url)

            await ctx.send(embed=embd)


def setup(bot: commands.Bot):
    bot.add_cog(HelpCommand(bot))
