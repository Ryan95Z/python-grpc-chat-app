import grpc
import src.server.chat_pb2 as chat_pb2
import src.server.chat_pb2_grpc as chat_pb2_grpc

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatStub(channel)
    r = stub.connect(chat_pb2.ChatUser(username='Ryan'))
    # print(r)

if __name__ == '__main__':
    main()
