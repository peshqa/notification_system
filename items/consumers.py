import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # логирование для отладки
        print(f"CONNECT ATTEMPT: User={self.scope['user']}")
        
        # Проверка аутентификации
        if self.scope["user"].is_anonymous:
            print("REJECTED: Anonymous user")
            await self.close(code=4001)
            return
        
        # Пользователь аутентифицирован
        self.user = self.scope["user"]
        self.group_name = f'user_{self.user.id}'
        print(f"CONNECTED: User={self.user.username}, Group={self.group_name}")
        
        # Добавляем в группу
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
    
        await self.accept()
        print("WebSocket ACCEPTED")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        print("Received message:", text_data)

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message']
        }))