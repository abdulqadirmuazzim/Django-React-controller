from rest_framework import generics, status
from rest_framework.views import APIView
from .models import Room
from .serializer import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from spotify.models import SpotifyToken


# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class JoinRoom(APIView):

    def post(self, req, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = self.request.data.get("code")
        if code:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                room = room[0]
                self.request.session["room_code"] = code
                return Response({"message": "Room Joined"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Bad Request": "Invalid Code, Room doesn't exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Bad Request": "Invalid data posted, couldn't find code"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"

    def get(self, req, format=None):
        code = req.GET.get(
            self.lookup_url_kwarg
        )  # use .get otherwise you'll get MultivalueDictKey error
        if code:
            room = Room.objects.filter(code=code)
            if room.exists():
                data = RoomSerializer(room[0]).data
                data["is_host"] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"Room Not Found": "Invalid Code"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    "Bad Request": f"{self.lookup_url_kwarg} parameter not found in request"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, req, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid():
            guest_pause = serializer.data["guest_pause"]
            vote_skip = serializer.data["votes_skip"]
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            # let's experiment a little bit
            print(self.request.session.serializer)

            if queryset.exists():
                room = queryset[0]
                room.guest_pause = guest_pause
                room.votes_skip = vote_skip
                room.save()
                self.request.session["room_code"] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_pause=guest_pause, votes_skip=vote_skip)
                room.save()
                self.request.session["room_code"] = room.code
                return Response(
                    RoomSerializer(room).data, status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"Bad Request": "Invalid data..."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserinRoom(APIView):

    def get(self, req, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = self.request.session.get("room_code")
        room_obj = Room.objects.filter(code=code)
        print(code)

        if room_obj.exists():
            print(room_obj[0])
            data = {"code": code}
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            return Response(
                "Not found: Room code doesn't exist", status=status.HTTP_404_NOT_FOUND
            )


class LeaveRoom(APIView):
    def post(self, req, format=None):
        print(req.GET, req.POST)
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host_id = self.request.session.session_key

            rooms = Room.objects.filter(host=host_id)
            spotify_token = SpotifyToken.objects.filter(user=host_id)
            if rooms.exists() and spotify_token.exists():
                room = rooms[0]
                print(host_id == room.host)
                spotify_token[0].delete()
                room.delete()
                return Response(
                    {"Message": "Room successfully deleted"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"Message": "Room doesn't exist"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"Message": "Room doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, req, format=None):
        # For new users or users with no session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            guest_pause = serializer.data.get("guest_pause")
            votes_skip = serializer.data.get("votes_skip")
            code = serializer.data.get("code")

            queryset = Room.objects.filter(code=code)
            if queryset.exists():
                room = queryset[0]
                user = self.request.session.session_key
                if room.host != user:
                    return Response(
                        {"Forbidden": "You're not allowed in this room"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                else:
                    room.guest_pause = guest_pause
                    room.votes_skip = votes_skip
                    room.save()
                    return Response(RoomSerializer(room).data, status.HTTP_200_OK)
            else:
                return Response(
                    {"Not Found": "Could not find this room"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            return Response(
                {"Bad request": "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST
            )
