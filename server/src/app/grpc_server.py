# app/grpc_server.py
import grpc
from concurrent import futures
import sys
import os
from src.generated import login_pb2
from src.generated import login_pb2_grpc
from use_cases.login_use_case import LoginUseCase
from src.infrastucture.user_repository import MySQLUserRepository

class Greeter(login_pb2_grpc.GreeterServicer):
    def __init__(self, login_use_case: LoginUseCase):
        self.login_use_case = login_use_case

    def Login(self, request, context):
        print(f"Recibida solicitud de login: usuario={request.user}")
        if not self.login_use_case.login(request.user, request.password):
            print("Autenticación fallida")
            context.set_details("Login failed!")
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return login_pb2.LoginResponse(message="Login failed!")
        print("Autenticación exitosa")
        return login_pb2.LoginResponse(message="Login successful")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    login_use_case = LoginUseCase(MySQLUserRepository())
    login_pb2_grpc.add_GreeterServicer_to_server(Greeter(login_use_case), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    server.wait_for_termination()
