from discord.ext import commands
from discord import Message

from helpers import general_helper, auth_helper
from managers import mongo_manager
from config import ANILIST_LOGIN, ANILIST_ID, BULLET_EMOTE, LOADING_EMOTE, YUI_SHY_EMOTE

class AuthModule(commands.Cog):

    @commands.command(name="register", aliases=["login"], description="Login with Anilist to enable more features")
    async def login(self, ctx:commands.Context):

        bot:commands.Bot = ctx.bot

        def check_user_message(msg:Message):
            return msg.author == ctx.author

        await ctx.reply(f"Check DM {YUI_SHY_EMOTE}")

        anilistID = None
        token = None
        trials = 0
        max_trials = 3

        while(max_trials - trials > 0):
            trials += 1

            auth_embd = await general_helper.get_information_embed(
                title="Login with your AniList Account",
                description="Send your AniList Username after this message.\n**Send `stop` to stop the OAuth process.**"
            )

            await ctx.author.send(embed=auth_embd)

            username_msg:Message = await bot.wait_for("message", check=check_user_message, timeout=100)

            if username_msg.content == "stop":
                await ctx.author.send("Authentication Stopped", reference=username_msg)
                return
            else:
                finding_account_msg:Message = await ctx.author.send(f"Finding account {LOADING_EMOTE}")

            fetched_id = await general_helper.get_id_from_anilist_username(username_msg.content)

            await finding_account_msg.delete()

            if fetched_id is None:
                not_found = await general_helper.get_information_embed(
                    title="Profile Not Found",
                    description=f"Make sure your username is correct.",
                )
                await ctx.author.send(embed=not_found)
                continue
            else:
                profile_embd = await auth_helper.get_user_from_anilistID(str(fetched_id))
                
                await ctx.author.send(embed=profile_embd)

                confirmation:Message = await bot.wait_for("message", check=check_user_message, timeout=100)

                if confirmation.content.lower().strip() == "yes" or confirmation.content.lower().strip() == "y":
                    anilistID = fetched_id
                    break
                elif confirmation.content.lower().strip() == "no" or confirmation.content.lower().strip() == "n":
                    continue

        if anilistID is None:
            await ctx.author.send("Maximum Attempts Reached! Authentication Terminated.")
            return

        auth_embd = await general_helper.get_information_embed(
            title="Login with your AniList Account",
            description="**Steps (read carefully)** \n" +
                        f"{BULLET_EMOTE} 1. Click on this [link]({ANILIST_LOGIN.format(client_id=ANILIST_ID)}) \n" +
                        f"{BULLET_EMOTE} 2. Enter your details and click Authorize. \n"+ 
                        f"{BULLET_EMOTE} 3. Copy the token and send it **here** after this message\n\n" +
                        "__**Note**__ : You can terminate the login process by sending `stop` instead of the token."  
        )

        await ctx.author.send(embed=auth_embd)
        waiter = await ctx.author.send(f"Waiting for TOKEN {LOADING_EMOTE}")

        token_msg = await bot.wait_for('message', check=check_user_message)

        await waiter.delete()

        if token_msg.content == "stop":
            await ctx.author.send("Maximum Trials Reached! Authentication Stopped")
            return
        else:
            token = token_msg.content
            await ctx.author.send("TOKEN RECEIVED!")
            await ctx.author.send("**Please delete this message now for your own safety!**", reference=token_msg)

        await ctx.author.send(f"Authentication Successful {YUI_SHY_EMOTE}")

        await mongo_manager.manager.add_user(str(ctx.author.id), anilistID, token)

def setup(bot:commands.Bot):
    bot.add_cog(AuthModule())
