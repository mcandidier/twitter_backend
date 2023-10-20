import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# from django.contrib.sessions.middleware import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twitter.settings')
django_asgi_app = get_asgi_application()

from django.urls import re_path
from notification import consumers
from notification.urls import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})

app = application
