from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.RoomView.as_view()),
    path("create", v.CreateRoomView.as_view()),
]
