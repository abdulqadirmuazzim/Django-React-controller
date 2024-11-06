import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os

dotenv.load_dotenv()

# variables
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_url = "http://127.0.0.1:8000/spotify/redirect"

scope = (
    "user-read-playback-state user-modify-playback-state user-read-currently-playing"
)
