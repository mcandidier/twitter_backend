from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.auth import AuthMiddleware, AuthMiddlewareStack, UserLazyObject
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware

from rest_framework.authtoken.models import Token

User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        token = Token.objects.get(key=token)
        return token.user
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        headers = {key.decode(): value.decode() for key, value in scope['headers']}
        scope['user'] = await get_user(headers['authorization'])
        return await self.app(scope, receive, send)

