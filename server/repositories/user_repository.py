from sqlalchemy.orm import Session
from server.entities.user import User


class UserRepository:
    def __init__(self, session: Session):
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

    def search_user(self, username: str) -> User:
        return self.session.query(User).filter(User.username == username).first()

    def update_user(self,  username: str, password: str = None, first_name: str = None, last_name: str = None, enabled: bool = None,):
        if not username:
            raise ValueError("username is required to update a user.")

        user = self.session.query(User).filter(
            User.username == username).first()
        if not user:
            raise ValueError(f"User with username {username} not found.")

        # Actualizar solo si se proporciona un nuevo valor y no es None ni vacío
        if password not in [None, ""]:
            user.password = password
        if first_name not in [None, ""]:
            user.first_name = first_name
        if last_name not in [None, ""]:
            user.last_name = last_name
        if enabled is not None:         # Esto permite True y False
            user.enabled = enabled

        try:
            self.session.commit()
            self.session.refresh(user)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while updating the user with username {
                               username}: {str(e)}")

        return user
