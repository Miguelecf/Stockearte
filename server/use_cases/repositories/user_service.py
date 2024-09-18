#user_service.py
import sys
import os
import concurrent.futures as futures
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../generated'))

import grpc
import user_pb2
import user_pb2_grpc
from sqlalchemy.orm import Session
from server.entities.user import User
from server.entities.base import SessionLocal
from server.repositories.user_repository import UserRepository
from server.use_cases.create_user import CreateUserUseCase
from server.use_cases.login_user import LoginUserCase

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