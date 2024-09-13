# use_cases/login_use_case.py
from domain.interfaces import UserRepositoryInterface

class CreateUser:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, username: str, password: str) -> bool:
        success = self.user_repository.create_user(username, password)
        if not success:
            return False
        return True