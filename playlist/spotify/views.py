from django.shortcuts import redirect, HttpResponse
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .util import update_or_create, is_authenticated
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_url = "http://127.0.0.1:8000/spotify/redirect"
scopes = (
    "user-read-playback-state user-modify-playback-state user-read-currently-playing"
)


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

        url = (
            Request(
                "GET",
                "https://accounts.spotify.com/authorize",
                params={
                    "scope": scopes,
                    "response_type": "code",
                    "redirect_uri": redirect_url,
                    "client_id": client_id,
                },
            )
            .prepare()
            .url
        )

        return Response({"url": url}, status=status.HTTP_200_OK)


# Getting the access token in the callback function
def spotify_callback(request, format=None):
    code = request.GET.get("code")
    error = request.GET.get("error")
    print(code)

    info = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_url,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    print(info)
    if info.ok:
        response = info.json()

        access_token = response.get("access_token")
        token_type = response.get("token_type")
        refresh_token = response.get("refresh_token")
        expires_in = response.get("expires_in")

        if not request.session.exists(request.session.session_key):
            request.session.create()

        update_or_create(
            request.session.session_key,
            access_token,
            token_type,
            expires_in,
            refresh_token,
        )

        return redirect("frontend:Home")
    else:
        return HttpResponse("Error: Access denied")


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_auth = is_authenticated(self.request.session.session_key)
        return Response({"status": is_auth}, status=status.HTTP_200_OK)
