from repositories.user_repository import UserRepository
from server.entities.user import User
from server.generated.user_pb2 import LoginRequest

class LoginUserCase:
    def __init__(self,user_repository: UserRepository):
        self.user_repository = user_repository
        
    def execute(self, request: LoginRequest) -> User:
            username = request.username
            password = request.password
            
            # Retrieve the user from the database using username
            user = self.user_repository.get_user_by_username(username)
            
            if user:
                # Check if the provided password matches (plain text comparison)
                if user.password == password:
                    return user
                else:
                    raise ValueError("Invalid password")
            else:
                raise ValueError("User not found")
