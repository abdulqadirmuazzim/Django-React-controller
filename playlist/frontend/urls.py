from django.urls import path
from . import views as v

urlpatterns = [
    path("", v.index, name="Home"),
    path("join", v.index),
    path("create", v.index),
]
