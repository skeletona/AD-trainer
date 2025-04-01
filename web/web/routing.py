from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from web import consumers

websocket_urlpatterns = [
    re_path(r"ws$", AuthMiddlewareStack(
        consumers.Consumer.as_asgi()),  # оберни Consumer с AuthMiddlewareStack
    ),
]