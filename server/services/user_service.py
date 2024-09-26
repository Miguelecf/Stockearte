#user_service.py
import sys
import os
import concurrent.futures as futures
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../generated'))

import grpc
from generated import user_pb2
from generated import user_pb2_grpc
from sqlalchemy.orm import Session
from server.entities.user import User
from server.entities.base import SessionLocal
from server.repositories.user_repository import UserRepository
from server.use_cases.create_user import CreateUserUseCase
from server.use_cases.login_user import LoginUserCase
from server.use_cases.search_user import SearchUserUseCase

class UserService(user_pb2_grpc.UserService):
    def __init__(self):
        self.db: Session = SessionLocal()  # Reemplaza con tu base de datos
        self.user_repository = UserRepository(self.db)  # Inicializa el repositorio
        self.create_user_use_case = CreateUserUseCase(self.user_repository)  # Inicializa el caso de uso# In-memory storage for users (replace with a database in a real-world scenario)

    def CreateUser(self, request, context):
        # Crear un objeto CreateUserRequest
        create_user_request = user_pb2.CreateUserRequest(
            username=request.username,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
            enabled=request.enabled,
            store_id=request.store_id
        )
    
    # Call the CreateUserUseCase
        try:
                user = self.create_user_use_case.execute(create_user_request)
                return user_pb2.User(
                    id=user.id,
                    username=user.username,
                    password=user.password,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    enabled=user.enabled,
                    store_id=user.store_id,
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return user_pb2.User()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return user_pb2.User()


    def Login(self, request, context):
        # Initialize the login use case
        login_user_case = LoginUserCase(self.user_repository)
        
        try:
            # Execute the login process
            user = login_user_case.execute(request)
            
            # Return the user information if login is successful
            return user_pb2.User(
                id=user.id,
                username=user.username,
                password=user.password,  # Remember this is plain text for now
                first_name=user.first_name,
                last_name=user.last_name,
                enabled=user.enabled,
                store_id=user.store_id
            )
        except ValueError as e:
            # Handle invalid login attempts (e.g., wrong username/password)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return user_pb2.User()
        except Exception as e:
            # Handle any unexpected errors
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return user_pb2.User()
        
    def SearchUser(self, request, context):
        # Aquí implementamos la búsqueda del usuario
        search_user_case = SearchUserUseCase(self.user_repository)

        try:
            # Ejecutar el caso de uso de búsqueda
            user = search_user_case.execute(request.username)

            # Retornar la información del usuario si se encuentra
            return user_pb2.User(
                id=user.id,
                username=user.username,
                password=user.password,  # Recuerda, esto es solo temporal
                first_name=user.first_name,
                last_name=user.last_name,
                enabled=user.enabled,
                store_id=user.store_id
            )
        except ValueError as e:
            # Manejar el caso de que no se encuentre el usuario
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            return user_pb2.User()
        except Exception as e:
            # Manejar errores inesperados
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return user_pb2.User()
        
        
    def UpdateUser(self, request: user_pb2.UpdateUserRequest, context: grpc.ServicerContext) -> user_pb2.User:
        # Validar que el username no esté vacío
        username = request.username
        if not username:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("The username field cannot be empty.")
            return user_pb2.User()  

        if all(param is None for param in [request.password, request.first_name, request.last_name, request.enabled]):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("At least one field to update must be provided.")
            return user_pb2.User()  

        try:
            updated_user = self.user_repository.update_user(
                username    = username,
                password    = request.password,
                first_name  = request.first_name,
                last_name   = request.last_name,
                enabled     = request.enabled
            )

            return user_pb2.User(            
                username    = updated_user.username,
                password    = updated_user.password,
                first_name  = updated_user.first_name,
                last_name   = updated_user.last_name,
                enabled     = updated_user.enabled
            )

        except ValueError as ve:
            print(f"Validation error: {str(ve)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(ve))
            return user_pb2.User()  # Devuelve User vacío

        except Exception as e:
            print(f"Unexpected error during user update: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An error occurred while updating the user: {str(e)}")
            return user_pb2.User()  # Devuelve User vacío    