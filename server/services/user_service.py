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
            is_central = request.is_central,
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
                    is_central = user.is_central,
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
            return user_pb2.LoginResponse(
                username=user.username, # Remember this is plain text for now
                first_name=user.first_name,
                last_name=user.last_name,
                enabled=user.enabled,
                is_central = user.is_central,
                store_id=user.store_id
            )
        except ValueError as e:
            # Handle invalid login attempts (e.g., wrong username/password)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return user_pb2.LoginResponse()
        except Exception as e:
            # Handle any unexpected errors
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return user_pb2.LoginResponse()
        
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
        
        
    def UpdateUser(self, request: user_pb2.User, context: grpc.ServicerContext) -> user_pb2.User:
        # Validar que el id no esté vacío
        user_id = request.id
        if not user_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("The id field cannot be empty.")
            return user_pb2.User()

        if all(param is None for param in [request.username, request.password, request.first_name, request.last_name, request.enabled, request.is_central, request.store_id]):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("At least one field to update must be provided.")
            return user_pb2.User()

        try:
            # Buscar el usuario por ID
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"User with ID {user_id} not found.")
                return user_pb2.User()

            # Actualizar solo los campos que se proporcionen
            if request.username:
                user.username = request.username
            if request.password:
                user.password = request.password
            if request.first_name:
                user.first_name = request.first_name
            if request.last_name:
                user.last_name = request.last_name
            if request.enabled is not None:
                user.enabled = request.enabled
            if request.is_central is not None:
                user.is_central = request.is_central
            if request.store_id:
                user.store_id = request.store_id

            # Guardar los cambios en el repositorio
            updated_user = self.user_repository.update_user(
                user_id=user.id,  # o user_id según tu lógica
                username=request.username,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name,
                enabled=request.enabled
            )

            # Retornar el usuario actualizado
            return user_pb2.User(
                id=updated_user.id,
                username=updated_user.username,
                password=updated_user.password,
                first_name=updated_user.first_name,
                last_name=updated_user.last_name,
                enabled=updated_user.enabled,
                is_central=updated_user.is_central,
                store_id=updated_user.store_id
            )

        except ValueError as ve:
            print(f"Validation error: {str(ve)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(ve))
            return user_pb2.User()

        except Exception as e:
            print(f"Unexpected error during user update: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occurred while updating the user: {str(e)}")
            return user_pb2.User()    
        
    def AssignStoreToUser(self, request: user_pb2.AssignStoreToUserRequest, context: grpc.ServicerContext) -> user_pb2.User:
        user_id = request.user_id
        
        if not user_id:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("The user_id field cannot be empty")
            return user_pb2.User()
        
        try:
            # Asignar la tienda al usuario
            user_store = self.user_repository.assign_store_to_user(
                user_id=user_id,
                store_code=request.store_code
            )
            
            # Después de asignar la tienda, obtener al usuario completo
            user = self.user_repository.get_user_by_id(user_id=user_id)

            # Devolver el usuario mapeado al objeto gRPC
            return user_pb2.User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                enabled=user.enabled,
                store_id=user.store_id  # O el código de la tienda si es necesario
            )
        
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Error: {str(e)}")
            return user_pb2.User()
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return user_pb2.User()     
        
    def SearchUserByStore(self, request: user_pb2.SearchUserByStoreRequest, context: grpc.ServicerContext) -> user_pb2.UserListResponse:
        store_code = request.store_code
        
        if not store_code:
            raise ValueError("The store_code field cannot be empty")
        
        found_users = self.user_repository.search_users_by_store(
            store_code=store_code
        )
        
        response = user_pb2.UserListResponse()
        
        for user in found_users:
            # Añadir cada usuario a la respuesta, omitiendo la contraseña
            user_message = user_pb2.User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                enabled=user.enabled,
                store_id=user.store_id,
            )
            response.users.append(user_message)  # Asumiendo que 'users' es una lista en UserListResponse

        return response
    
    def ListUsers(self, request: user_pb2.UserListRequest, context: grpc.ServicerContext) -> user_pb2.UserListResponse:
        users = self.user_repository.list_users()
        if not users:
            raise ValueError("No users found.")
        
        response = user_pb2.UserListResponse()
        for user in users:
            user_message = user_pb2.User(
                id=user.id,
                username=user.username,
                password= user.password,
                first_name=user.first_name,
                last_name=user.last_name,
                enabled=user.enabled,
                is_central=user.is_central,
                store_id=user.store_id,
            )
            response.users.append(user_message)
        return response

            