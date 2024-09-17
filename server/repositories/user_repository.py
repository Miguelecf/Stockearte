from sqlalchemy.orm import Session
from server.entities.user import User

class UserRepository:
    def __init__(self,session: Session):
        self.session = session
        
    def create_user(self, username: str, password: str, first_name: str, last_name: str, enabled: bool, store_id: int) -> User:
        # Handle case where store_id is zero or invalid by setting it to None
        store_id = None if store_id <= 0 else store_id

        # Create a new User object
        user = User(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            enabled=enabled,
            store_id=store_id
        )

        # Add the user to the database session
        self.session.add(user)

        # Commit the changes to the database
        self.session.commit()

        # Return the newly created user
        return user
    
    def get_user_by_username(self, username: str) -> User:
        
        return self.session.query(User).filter(User.username == username).first()