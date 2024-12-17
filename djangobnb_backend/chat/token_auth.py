from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from rest_framework_simplejwt.tokens import AccessToken

from useraccount.models import User

@database_sync_to_async
def get_user (token_key):
    try:
        token = AccessToken(token_key)
        user_id = token.payload["user_id"]
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return AnonymousUser

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extract the query string parameters
        query = dict(x.split("=") for x in scope["query_string"].decode().split("&"))

        # Get the token and fetch user data
        token_key = query.get('token')
        scope["user"] = await get_user(token_key)

        # Call the inner application
        return await self.inner(scope, receive, send)