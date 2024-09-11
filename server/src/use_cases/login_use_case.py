# use_cases/login_use_case.py
from domain.interfaces import UserRepositoryInterface

class LoginUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def login(self, username: str, password: str) -> bool:
        user = self.user_repository.get_user_by_username(username)
        print(user)
        if not user or user.password != password or not user.enabled:
            return False
        return True