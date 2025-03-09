from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post
import requests as req
import os
import dotenv

dotenv.load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URL = os.environ.get("REDIRECT_URL")

Base_url = "https://api.spotify.com/v1/me/"


def get_token(session_id):
    user_token = SpotifyToken.objects.filter(user=session_id)
    if user_token.exists():
        return user_token[0]
    else:
        return None


def update_or_create(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_token(session_id=session_id)
    expires = timezone.now() + timedelta(seconds=expires_in)
    print("Expiry Datetime of the token:", expires)
    print("Type of expiry Datetime of the token:", type(expires))

    if tokens:
        # Update the current tokens
        tokens.access = access_token
        tokens.refresh = refresh_token
        tokens.expires = expires
        tokens.token_type = token_type
        tokens.save()
    else:
        tokens = SpotifyToken.objects.create(
            user=session_id,
            access=access_token,
            refresh=refresh_token,
            expires=expires,
            token_type=token_type,
        )
        tokens.save()


def is_authenticated(session_id):
    tokens = get_token(session_id)
    if tokens:
        expiry = tokens.expires
        if expiry <= timezone.now():
            refresh_token(session_id)
        return True
    else:
        return False


def refresh_token(session_id):
    refresh_token = get_token(session_id).refresh
    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json()
    access_token = response.get("access_token")
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")

    print("Response type", response)
    print("Refesh Token:", response.get("refresh_token"))
    if not refresh_token:
        get_token(session_id).delete()
        update_or_create(
            session_id, access_token, token_type, expires_in, refresh_token
        )

    update_or_create(session_id, access_token, token_type, expires_in, refresh_token)


def spotify_request(session_id, endpoint: str, post_=False, put_=False):
    tokens = get_token(session_id)
    header = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {tokens.access}",
    }
    if post_:
        response = post(Base_url + endpoint, headers=header)

    elif put_:
        response = req.put(Base_url + endpoint, headers=header)

    else:
        response = req.get(Base_url + endpoint, headers=header)

    try:
        return response.json()
    except:
        return {
            "Error": "Something went wrong, maybe try checking your connection",
            "Status": response.status_code,
        }


# function to play a song
def play_song(session_id):
    return spotify_request(session_id, "player/play", put_=True)


# function to pause a song
def pause_song(session_id):
    return spotify_request(session_id, "player/pause", put_=True)


def skip_song(session_id):
    return spotify_request(session_id, "player/next", post_=True)
