from discord.ui import Button, View
from discord import ButtonStyle

from helpers.spotify_helper import SpotifyTrackAlternative
from config import YOUTUBE_VIDEO_EMOTE, YOUTUBE_MUSIC_EMOTE

class SpotifyView(View):

    def __init__(self, links:SpotifyTrackAlternative, timeout: int = 30):
        super().__init__(timeout=timeout)

        video_btn: Button = Button(label="YOUTUBE VIDEO", style=ButtonStyle.green, url=links.youtube_video, emoji=YOUTUBE_VIDEO_EMOTE)
        music_btn: Button = Button(label="YOUTUBE MUSIC", style=ButtonStyle.green, url=links.youtube_music, emoji=YOUTUBE_MUSIC_EMOTE)

        video_btn.disabled = False if links.youtube_video is not None else True
        music_btn.disabled = False if links.youtube_music is not None else True

        self.add_item(video_btn)
        self.add_item(music_btn)
            