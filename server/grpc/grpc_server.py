import sys
import os
import concurrent.futures as futures

# Insert the parent directory of the current script into the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import services from the parent directory
from server.services import user_service
from server.services import store_service

import grpc
import generated.user_pb2 as user_pb2
import generated.user_pb2_grpc as user_pb2_grpc
import generated.store_pb2 as store_pb2
import generated.store_pb2_grpc as store_pb2_grpc

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(user_service.UserService(), server)
    store_pb2_grpc.add_StoreServiceServicer_to_server(store_service.StoreService(),server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()