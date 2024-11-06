from django.db import models


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh = models.CharField(max_length=150)
    access = models.CharField(max_length=150)
    expires = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}"
