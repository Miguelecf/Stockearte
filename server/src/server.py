import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))
import grpc
from concurrent import futures
import login_pb2
import login_pb2_grpc

class Greeter(login_pb2_grpc.GreeterServicer):
    def Login(self, request, context):
        print(f"Recibida solicitud de login: usuario={request.user}")
        if not self._validate_user(request.user, request.password):
            print("Autenticación fallida")
            context.set_details("Login failed!")
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return login_pb2.LoginResponse() 
        print("Autenticación exitosa")
        return login_pb2.LoginResponse(message="Login successful")

    def _validate_user(self, user, password):
        return user == "admin" and password == "admin"

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    login_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
