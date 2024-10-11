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
