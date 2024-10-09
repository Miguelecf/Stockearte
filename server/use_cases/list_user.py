from typing import List  # Importa List de typing
from repositories.user_repository import UserRepository
from server.entities.user import User
from server.generated.user_pb2 import UserListRequest

class ListUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    def execute(self) -> list[User]:
        users = self.user_repository.list_users()
        if not users:
            raise ValueError("User list not found.")
        return user  