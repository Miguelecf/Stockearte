from repositories.user_repository   import UserRepository
from server.entities.user           import User
from server.generated.user_pb2      import User

class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, username: str, password: str = None, first_name: str = None, last_name: str = None, enabled: bool = None) -> User:
        return self.user_repository.update_user(username, password, first_name, last_name, enabled)