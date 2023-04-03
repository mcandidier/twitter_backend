import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from twitter.middleware import TokenAuthMiddleware
from django.contrib.sessions.middleware import SessionMiddleware


from notification.urls import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns),
        )
    )
})
