from django.contrib import admin
from .models import SpotifyToken, Vote

# Register your models here.

admin.site.register(SpotifyToken)
admin.site.register(Vote)
