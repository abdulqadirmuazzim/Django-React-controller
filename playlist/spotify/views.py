from django.shortcuts import redirect, HttpResponse, get_object_or_404
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from track.models import Room
from .models import Vote
from .util import (
    update_or_create,
    is_authenticated,
    spotify_request,
    pause_song,
    play_song,
    skip_song,
)
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


class Currentsong(APIView):
    def get(self, req, format=None):
        room_code = self.request.session.get("room_code")
        room = get_object_or_404(Room, code=room_code)
        host = room.host
        endpoint = "player/currently-playing"
        # send a get request
        response = spotify_request(host, endpoint)
        # we check if "Error" is in response or in item is not in response or if item is null
        if "Error" in response or "item" not in response:
            return Response(
                {"error": "response didn't return any content"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            item = response.get("item")
            duration = item.get("duration_ms")
            progress = response.get("progress_ms")
            album_cover = item.get("album").get("images")[0].get("url")
            is_playing = response.get("is_playing")
            song_id = item.get("id")

            artist_string = ""
            for i, artist in enumerate(item.get("artists")):
                if i > 0:
                    name = artist.get("name")
                    artist_string += f"{name}, "
            votes = Vote.objects.filter(room=room, song_id=song_id)
            votes = len(votes)
            song = {
                "item": item.get("name"),
                "artists": artist_string,
                "duration": duration,
                "time": progress,
                "image_url": album_cover,
                "is_playing": is_playing,
                "votes": votes,
                "required_votes": room.votes_skip,
                "id": song_id,
            }
            self.update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)

    def update_room_song(self, room, song_id):
        current = room.current_song

        if current != song_id:
            room.current_song = song_id
            room.save()
            votes = Vote.objects.filter(room=room)
            votes.delete()


class PauseSong(APIView):
    def put(self, res):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "Error": "You are not allowed to perform this action,\neither you're not the host or you not using a premium accout "
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class PlaySong(APIView):
    def put(self, res):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {
                    "Error": "You are not allowed to perform this action,\neither you're not the host or you not using a premium accout "
                },
                status=status.HTTP_403_FORBIDDEN,
            )


# skipping song
class SkipSong(APIView):
    def post(self, req):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code=room_code)

        if room.exists():
            room = room[0]
            votes = Vote.objects.filter(room=room, song_id=room.current_song)
            votes_needed_to_skip = room.votes_skip

            if (self.request.session.session_key == room.host) or (
                len(votes) + 1 >= votes_needed_to_skip
            ):
                skip_song(room.host)
                votes.delete()
                return Response({"Success: Skipped"}, status=status.HTTP_204_NO_CONTENT)
            else:
                Vote.objects.create(
                    user=self.request.session.session_key,
                    room=room,
                    song_id=room.current_song,
                )
                # vote.save()
                return Response(
                    {"Success: Added votes to skip song"},
                    status=status.HTTP_204_NO_CONTENT,
                )
        else:
            return Response({"Error: Room not found"}, status=status.HTTP_404_NOT_FOUND)
