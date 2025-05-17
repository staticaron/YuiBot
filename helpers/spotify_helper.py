import asyncio

from discord import Message
import pyyoutube
import ytmusicapi
import spotipy

import config


class SpotifyTrackAlternative:
    track_name: str = None

    track_artists: str = None

    youtube_video: str = None

    youtube_music: str = None

    apple_music: str = None

    amazon_music: str = None


async def youtube_fetch(track_name: str, track_artists: str):
    """Fetch youtube video based on track_name and track_artists"""

    youtube_client = pyyoutube.Api(api_key=config.YOUTUBE_API_KEY)

    youtube_track = youtube_client.search_by_keywords(
        q="{} {}".format(track_name, track_artists),
        search_type=["video"],
        count=1,
        limit=1,
    )

    return youtube_track


async def youtube_music_fetch(track_name: str, track_artists: str):
    """Fetch music video from youtube music based on track name and artist name"""

    youtube_music_client = ytmusicapi.YTMusic()

    result = youtube_music_client.search("{} {}".format(track_name, track_artists), filter="songs", limit=1)
    return result


def fetch_spotipy(track_id):
    """Fetch the track details from spotify"""

    auth_manager = spotipy.SpotifyClientCredentials(client_id=config.SPOTIFY_CLIENT_ID, client_secret=config.SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp.track(track_id)


async def get_alternatives(message: Message, spotify_track_id: str) -> SpotifyTrackAlternative:
    """Get alternative links to the current spotify song"""

    links: SpotifyTrackAlternative = SpotifyTrackAlternative()

    spotify_track = await asyncio.to_thread(fetch_spotipy, spotify_track_id)

    all_artists: list[str] = []

    for artist_details in spotify_track.get("artists"):
        all_artists.append(artist_details.get("name"))

    links.track_name = spotify_track.get("name")

    links.track_artists = " - ".join(all_artists)

    video_results = await youtube_fetch(links.track_name, links.track_artists)

    music_results = await youtube_music_fetch(links.track_name, links.track_artists)

    links.youtube_video = config.YOUTUBE_TRACK_BASE + video_results.items[0].id.videoId if len(video_results.items) > 0 else None

    links.youtube_music = config.YOUTUBE_MUSIC_BASE + music_results[0].get("videoId") if len(music_results) > 0 else None

    return links
