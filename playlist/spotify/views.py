from django.shortcuts import render, redirect
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_url = os.environ.get("REDIRECT_URL")


class AuthURL(APIView):
    def get(self, req, format=None):
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


def spotify_callback(req, format=None):
    code = req.GET.get("code")
    error = req.GET.get("error")

    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_url,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    ).json()

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    error = response.get("error")
    if not req.session.exists(req.session.session_key):
        req.session.create()

    update_or_create(
        session_id=req.session.session_key,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type=token_type,
    )
    return redirect("frontend:")
