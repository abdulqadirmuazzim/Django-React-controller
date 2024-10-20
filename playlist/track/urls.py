from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.RoomView.as_view()),
    path("create", v.CreateRoomView.as_view()),
    path("get-room", v.GetRoom.as_view()),
    path("join-room", v.JoinRoom.as_view()),
    path("user-in-room", v.UserinRoom.as_view()),
    path("leave-room", v.LeaveRoom.as_view()),
    path("update-room", v.UpdateRoom.as_view()),
]
