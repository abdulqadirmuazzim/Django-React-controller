from django.shortcuts import render, HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import Room
from .serializer import RoomSerializer, CreateRoomSerializer
from rest_framework.response import Response

# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"

    def get(self, req, format=None):
        code = req.GET.get(
            self.lookup_url_kwarg
        )  # use .get otherwise you'll get MultivalueDictKey error
        if code:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
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
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_pause=guest_pause, votes_skip=vote_skip)
                room.save()
                return Response(
                    RoomSerializer(room).data, status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                {"Bad Request": "Invalid data..."},
                status=status.HTTP_400_BAD_REQUEST,
            )
