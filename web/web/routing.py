from django.urls import re_path
from web import consumers

websocket_urlpatterns = [
    re_path(r"ws$", consumers.Consumer.as_asgi()),
]