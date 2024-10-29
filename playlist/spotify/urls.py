from django.urls import path
from . import views as v

urlpatterns = [
    path("get-auth-url", v.AuthURL.as_view()),
]
