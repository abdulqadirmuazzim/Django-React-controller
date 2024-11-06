from django.urls import path
from . import views as v

app_name = "frontend"

urlpatterns = [
    path("", v.index, name="Home"),
    path("join", v.index),
    path("create", v.index),
    path("room/<str:roomcode>", v.index),
    path("update-room/<str:roomcode>", v.index),
]
