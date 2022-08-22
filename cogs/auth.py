from discord.ext import commands
from discord import Message
from asyncio import TimeoutError

from views.confirmation_view import ConfirmationView
from managers import mongo_manager
from helpers import general_helper, auth_helper
from managers import mongo_manager
from helpers import general_helper, auth_helper
from config import ANILIST_LOGIN, ANILIST_ID, BULLET_EMOTE, LOADING_EMOTE, YUI_SHY_EMOTE


class AuthModule(commands.Cog):

    @commands.command(name="register", aliases=["login"], description="Login with Anilist to enable more features")
    @general_helper.short_cooldown()
    async def login(self, ctx: commands.Context):

        await ctx.trigger_typing()

        bot: commands.Bot = ctx.bot

        def check_user_message(msg: Message):
            return msg.author == ctx.author

        await ctx.reply(f"Check DM {YUI_SHY_EMOTE}")

        auth_embd = await general_helper.get_information_embed(
            title="Login with your AniList Account",
            description="**Steps (read carefully)** \n" +
                        f"{BULLET_EMOTE} 1. Click on this [link]({ANILIST_LOGIN.format(client_id=ANILIST_ID)}) \n" +
                        f"{BULLET_EMOTE} 2. Enter your details and click Authorize. \n" +
                        f"{BULLET_EMOTE} 3. Copy the token and send it **here** after this message\n\n" +
                        "__**Note**__ : You can terminate the login process by sending `stop` instead of the token."
        )

        await ctx.author.send(embed=auth_embd)
        waiter = await ctx.author.send(f"Waiting for TOKEN {LOADING_EMOTE}")

        try:
            token_msg = await bot.wait_for('message', check=check_user_message, timeout=300)
        except TimeoutError:
            await waiter.delete()
            await ctx.author.send("Authentication Timed Out. Please try again.")
            return

        await waiter.delete()

        if token_msg.content == "stop":
            await ctx.author.send("Authentication Stopped")
            return
        else:
            token = token_msg.content
            await ctx.author.send("TOKEN RECEIVED!")
            await ctx.author.send("**Please delete this message now for your own safety!**", reference=token_msg)

        await ctx.author.send(f"Authentication Successful {YUI_SHY_EMOTE}")

        anilistID = await general_helper.get_id_from_token(token)

        await mongo_manager.manager.add_user(str(ctx.author.id), anilistID, token)

    @commands.command(name="logout", description="Logout with your AniList account")
    @general_helper.short_cooldown()
    async def logout(self, ctx: commands.Context):

        await ctx.trigger_typing()

        confirmation_embd = await general_helper.get_information_embed(
            title="Are you sure?",
            description="Click `CONFIRM` to log out."
        )

        async def yes_callback(self):
            reply = await auth_helper.logout(str(ctx.author.id))

            await ctx.reply(embed=reply)

        async def no_callback(self):

            await ctx.reply("Logout Terminated. You are still logged in ^^.")
            return

        view = ConfirmationView(yes_callback, no_callback)

        await ctx.reply(embed=confirmation_embd, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(AuthModule())
