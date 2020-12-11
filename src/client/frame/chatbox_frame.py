import tkinter as tk
import src.server.chat_pb2 as chat_pb2
from src.client.grpc_client import GrpcClient
from src.client.frame.base import BaseChatFrame


class ChatboxFrame(BaseChatFrame):
    """Frame to accept a user's message and send to the chat server when send button is clicked"""

    def __init__(self, master, grpc_client, message_send_callback=None):
        """ChatboxFrame constructor

        Args:
            master:                 The parent tk component. Either a frame or tkinter Tk.
            grpc_client:            The grpc client wrapper to communicate with the server.
            message_send_callback:  Callback function that is triggered once a message is
                                    is sent to the server.
        """
        super(ChatboxFrame, self).__init__(master, grpc_client)
        self._message_send_callback = message_send_callback
        self.__set_up_widgets()

    def __set_up_widgets(self):
        self.__set_up_chatbox_widgets()
        self.__set_up_chat_send_btn_widget()

    def __set_up_chatbox_widgets(self):
        self.chat_box = tk.Text(self, height=5)
        self.chat_box.grid(row=0, column=0, columnspan=3)

    def __set_up_chat_send_btn_widget(self):
        self.send_btn = tk.Button(self, text='Send', height=5, width=20, command=self.__btn_action_send_message)
        self.send_btn.grid(row=0, column=4, columnspan=2, sticky=tk.EW)
        self.disable_send_btn()

    def __btn_action_send_message(self):
        message = self.__get_users_message()
        self.__clear_users_message_box()

        grpc_message = self.__construct_message_payload(message)
        self._grpc_client.send_message(grpc_message)
        if self._message_send_callback is not None:
            self._message_send_callback(message)

    def __get_users_message(self):
        return self.chat_box.get('1.0', 'end-1c')

    def __clear_users_message_box(self):
        self.chat_box.delete('1.0', 'end-1c')

    def __construct_message_payload(self, message):
        return chat_pb2.ChatMessage(
            userId=self._grpc_client.user_id,
            username=self._grpc_client.username,
            message=message
        )

    def enable_send_btn(self):
        """Enable the send button on the user interface"""
        self.send_btn['state'] = 'normal'

    def disable_send_btn(self):
        """Disable the send button on the user interface"""
        self.send_btn['state'] = 'disabled'
