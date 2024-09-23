from repositories.user_repository import UserRepository
from server.entities.user import User
from server.generated.user_pb2 import SearchUserRequest


class SearchUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
  
    def execute(self, username: str) -> User:
        # Llamar al repositorio para buscar el usuario por username
        user = self.user_repository.search_user(username)
        
        if not user:
            raise ValueError(f"User with username {username} not found.")
        
        return user  # Devolver el usuario encontrado
