# Define WebSocket URL patterns to be used by Channels for routing task-related communications

from django.urls import re_path  # Import re_path for regex based URL matching
from . import consumers  # Import consumers from the current module

websocket_urlpatterns = [
    re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),  # Define websocket URL for task updates
]