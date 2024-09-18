from server.repositories.user_repository import UserRepository
from server.entities.user import User
from generated.user_pb2 import CreateUserRequest

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, request: CreateUserRequest) -> User:
        # Validate the request
        if not request.username:
            raise ValueError("Username is required")
        if not request.password:
            raise ValueError("Password is required")
        if not request.first_name:
            raise ValueError("First name is required")
        if not request.last_name:
            raise ValueError("Last name is required")

        if request.store_id is not None and request.store_id < 0:
            raise ValueError("Store ID must be a non-negative integer or None")

        try:
            user = self.user_repository.create_user(
                username=request.username,
                password=request.password,
                first_name=request.first_name,
                last_name=request.last_name,
                enabled=request.enabled,
                store_id=request.store_id  # Handle None values in repository
            )
            return user
        except Exception as e:
            raise ValueError(f"Failed to create user: {str(e)}")
