import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os

dotenv.load_dotenv()

# variables
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_url = os.environ.get("REDIRECT_URL")


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_url,
        scope="user-top-read",
    )
)

tracks = sp.current_user_top_tracks(limit=5, time_range="short_term")

track_ids = [track[id] for track in tracks]

print(tracks)
