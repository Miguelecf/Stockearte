# app/grpc_server.py
import grpc
from concurrent import futures
from src.use_cases.create_user import CreateUser
from src.generated import login_pb2
from src.generated import login_pb2_grpc
from use_cases.login_use_case import LoginUseCase
from src.infrastucture.user_repository import MySQLUserRepository

class Greeter(login_pb2_grpc.GreeterServicer):
    def __init__(self, login_use_case: LoginUseCase,create_user: CreateUser):
        self.login_use_case = login_use_case
        self.create_user = create_user

    def Login(self, request, context):
        print(f"Recibida solicitud de login: usuario={request.user}")
        if not self.login_use_case.login(request.user, request.password):
            print("Autenticación fallida")
            context.set_details("Login failed!")
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return login_pb2.LoginResponse(message="Login failed!")
        print("Autenticación exitosa")
        return login_pb2.LoginResponse(message="Login successful")
    
    def CreateUser(self, request, context):
        print(f"Recibida solicitud de creación de usuario: usuario={request.username}")
        success = self.create_user.execute(request.username, request.password)
        if not success:
            print("Creación de usuario fallida")
            context.set_details("User creation failed!")
            context.set_code(grpc.StatusCode.INTERNAL)
            return login_pb2.CreateUserResponse(message="User creation failed!")
        print("Usuario creado exitosamente")
        return login_pb2.CreateUserResponse(message="User created successfully")
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    login_use_case = LoginUseCase(MySQLUserRepository())
    create_user = CreateUser(MySQLUserRepository())
    login_pb2_grpc.add_GreeterServicer_to_server(Greeter(login_use_case,create_user), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    server.wait_for_termination()
