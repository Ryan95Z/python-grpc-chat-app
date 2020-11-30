import grpc
import chat_pb2_grpc as chat_pb2_grpc
from chat_service import ChatService
from concurrent import futures

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Stopping Server')
        server.stop(0)

if __name__ == '__main__':
    main()