from channels.generic.websocket import AsyncWebsocketConsumer
import json
import redis

rooms = redis.Redis(host='127.0.0.1', port=6379)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global rooms
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if not rooms.get(self.room_group_name):
            rooms.set(self.room_group_name, json.dumps([]))

        users = json.loads(rooms[self.room_group_name])
        users.append(self.scope['user'].username)
        rooms.set(self.room_group_name, json.dumps(users))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.scope['user'].username + ' entered the room',
                'user': '~',
                'users_in_room': users,
            }
        )

    async def disconnect(self, close_code):
        global rooms

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        users: list = json.loads(rooms[self.room_group_name])
        if len(users) > 1:
            users.remove(self.scope['user'].username)
            rooms.set(self.room_group_name, json.dumps(users))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': self.scope['user'].username + ' left the room',
                    'user': '~',
                    'users_in_room': users,
                }
            )
        else:
            rooms.delete(self.room_group_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        global rooms
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        users_in_room: list = json.loads(rooms[self.room_group_name])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'users_in_room': users_in_room,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        users_in_room = event['users_in_room']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'users_in_room': users_in_room,
        }))
