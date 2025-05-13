from discord import Message
import aiospotify
import pyyoutube
import ytmusicapi

import config

class SpotifyTrackAlternative:
    youtube_video:str = None
    youtube_music:str = None
    apple_music:str = None
    amazon_music:str = None

async def youtube_fetch(track_name:str, track_artists:str):
    youtube_client = pyyoutube.Api(api_key=config.YOUTUBE_API_KEY)
    youtube_track = youtube_client.search_by_keywords(q="{} {}".format(track_name, track_artists), search_type=["video"], count=1, limit=1)
    return youtube_track

async def youtube_music_fetch(track_name:str, track_artists:str):
    youtube_music_client = ytmusicapi.YTMusic()
    result = youtube_music_client.search("{} {}".format(track_name, track_artists))
    return result

async def fetch_spotify_track(track_id):
    spotify_async_client:aiospotify.Aiospotify = aiospotify.Aiospotify(client_id=config.SPOTIFY_CLIENT_ID, client_secret=config.SPOTIFY_CLIENT_SECRET)
    spotify_auth_token:str = await spotify_async_client.init_auth()
    return spotify_async_client.search_track(id_=track_id, token=spotify_auth_token)

async def send_alternatives(message:Message, spotify_track_id:str) -> SpotifyTrackAlternative:

    links:SpotifyTrackAlternative = SpotifyTrackAlternative()

    # spotify_credentials:spotipy.SpotifyClientCredentials = spotipy.SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    # spotify_client:spotipy.Spotify = spotipy.Spotify(auth_manager=spotify_credentials)

    spotify_track = await fetch_spotify_track(spotify_track_id)

    all_artists:list[str] = []
    for artist_details in spotify_track.get("artists"):
        all_artists.append(artist_details.get("name"))
    
    track_name:str = spotify_track.get("name")
    track_artists:str = " - ".join(all_artists)

    video_results = await youtube_fetch(track_name, track_artists)
    music_results = await youtube_music_fetch(track_name, track_artists)

    links.youtube_video = config.YOUTUBE_TRACK_BASE + video_results.items[0].id.videoId if len(video_results.items) > 0 else None
    links.youtube_music = config.YOUTUBE_MUSIC_BASE + music_results[0].get("videoId") if len(music_results) > 0 else None
    
    return links


    