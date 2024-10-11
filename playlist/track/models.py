from django.db import models
import random
import string


def generate_code():
    length = 6
    i = 0
    while True:
        i += 1
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        if not code in Room.objects.all():
            break
        elif i == 100000:
            print("Tried 100000 times.")
            break

    return code


# next run migrations
class Room(models.Model):
    code = models.CharField(max_length=8, unique=True, default=generate_code)
    host = models.CharField(max_length=50, unique=True)
    guest_pause = models.BooleanField(null=False, default=False)
    votes_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.host)
