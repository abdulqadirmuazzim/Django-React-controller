from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.RoomView.as_view(), name="api"),
]
