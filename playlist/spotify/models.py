from django.db import models
from track.models import Room


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh = models.CharField(max_length=150)
    access = models.CharField(max_length=150)
    expires = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}"


# For Counting the number of votes we need to know the song we're voting for, the id of the users that voted,
# the room the users are at, then optionally the time of voting.


class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    song_id = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
