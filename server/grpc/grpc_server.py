import sys
import os
import concurrent.futures as futures

# Insert the parent directory of the current script into the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import services from the parent directory
from server.services import user_service
from server.services import store_service
from server.services import product_service
from server.services import product_store_service

import grpc
from generated import user_pb2 as user_pb2
from generated import user_pb2_grpc as user_pb2_grpc
from generated import store_pb2 as store_pb2
from generated import store_pb2_grpc as store_pb2_grpc
from generated import product_pb2 as product_pb2
from generated import product_pb2_grpc as product_pb2_grpc
from generated import product_store_pb2 as product_store_pb2
from generated import product_store_pb2_grpc as product_store_pb2_grpc
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(user_service.UserService(), server)
    store_pb2_grpc.add_StoreServiceServicer_to_server(store_service.StoreService(),server)
    product_pb2_grpc.add_ProductServiceServicer_to_server(product_service.ProductService(),server)
    product_store_pb2_grpc.add_ProductStoreServiceServicer_to_server(product_store_service.ProductStoreService(),server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()