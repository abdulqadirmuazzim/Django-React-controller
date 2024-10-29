from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta


def get_token(session_id):
    user_token = SpotifyToken.objects.filter(user=session_id)
    if user_token.exists():
        return user_token[0]
    else:
        return None


def update_or_create(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_token(session_id=session_id)
    expires = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        # Update the current tokens
        tokens.access = access_token
        tokens.refresh = refresh_token
        tokens.expires = expires_in
        tokens.token_type = token_type
        tokens.save()
    else:
        tokens = SpotifyToken.objects.create(
            user=session_id,
            access=access_token,
            refresh=refresh_token,
            expires=expires_in,
            token_type=token_type,
        )
        tokens.save()
