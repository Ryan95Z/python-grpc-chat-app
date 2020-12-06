import random
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        super(ChatService, self).__init__()
        self.chats = []
        self.users = {}
        self.stop_thread = False

    def connect(self, request, context):
        user_id = random.randint(1, 10000)
        self.users[user_id] = request.username
        return chat_pb2.ChatUserConnected(username=request.username, userId=user_id)

    def disconnect(self, request, context):
        del self.users[request.userId]
        return chat_pb2.ChatUserDisconnect(isDisconnected=True)

    def sendMessage(self, request, context):
        self.chats.append(request)
        return chat_pb2.ChatMessage(userId=request.userId, username=request.username)

    def subscribeMessages(self, request, context):
        current_user_id = request.userId
        last_seen_message_index = 0

        while (not self.stop_thread) and (self.users.get(current_user_id, None) != None):
            while len(self.chats) > last_seen_message_index:
                message = self.chats[last_seen_message_index]
                last_seen_message_index += 1
                if message.userId != current_user_id:
                    yield message
