from repositories.user_repository import UserRepository
from server.entities.user import User
from server.generated.user_pb2 import AssignStoreToUserRequest

class AssignStoreToUserUseCase:
    def __init__(self,user_repository: UserRepository):
        self.user_repository = user_repository
        
    
    def execute(self, request: AssignStoreToUserRequest) -> User:
        # Validar que el user_id y store_code están presentes en la solicitud
        if not request.user_id:
            raise ValueError("user_id is required")
        
        if not request.store_code:
            raise ValueError("store_code is required")

        try:
            # Llamar al método de asignación en el UserRepository
            user = self.user_repository.assign_store_to_user(
                user_id=request.user_id, 
                store_code=request.store_code
            )
            
            return user  # Devolver el usuario actualizado con la tienda asignada
        
        except ValueError as e:
            # Manejar casos donde el usuario o tienda no se encuentran
            raise ValueError(f"Failed to assign store to user: {str(e)}")

        except Exception as e:
            # Manejar errores generales
            raise RuntimeError(f"An error occurred during store assignment: {str(e)}")