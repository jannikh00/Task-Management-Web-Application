# Implement an asynchronous consumer to handle WebSocket connections for task updates, including group management for broadcasting messages

from channels.generic.websocket import AsyncWebsocketConsumer  # Import AsyncWebsocketConsumer for handling WebSocket connections
import json  # Import json to serialize/deserialize messages

class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()  # Accept the incoming connection
        # Add the user to a group for broadcasting messages
        await self.channel_layer.group_add("tasks_group", self.channel_name)  # Add this connection to the tasks group

    async def disconnect(self, close_code):
        # Remove the user from the group on disconnection
        await self.channel_layer.group_discard("tasks_group", self.channel_name)  # Remove connection from tasks group

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        data = json.loads(text_data)  # Parse the incoming JSON message
        # For example, if a task update is received, broadcast it to the group
        await self.channel_layer.group_send(
            "tasks_group",
            {
                'type': 'task_update',  # Custom event name for handling task updates
                'message': data  # Include the received data in the message
            }
        )

    async def task_update(self, event):
        # Send task update to WebSocket client
        message = event['message']  # Extract the message from the event
        await self.send(text_data=json.dumps(message))  # Send the message as a JSON string to the client