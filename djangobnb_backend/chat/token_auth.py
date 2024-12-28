from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework_simplejwt.tokens import AccessToken

from useraccount.models import User

@database_sync_to_async
def get_user(token_key):
    if not token_key:
        return AnonymousUser()
    try:
        token = AccessToken(token_key)
        user_id = token.payload.get("user_id")
        return User.objects.get(pk=user_id)
    except (User.DoesNotExist, KeyError):
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query = dict(param.split("=") for param in query_string.split("&"))
        token_key = query.get('token')
        scope["user"] = await get_user(token_key)
        return await super().__call__(scope, receive, send)