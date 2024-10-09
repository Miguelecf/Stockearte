import pymysql
from sqlalchemy.orm import Session
from server.entities.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str, first_name: str, last_name: str,
                enabled: bool, is_central: bool, store_id: int) -> User:
    # Handle case where store_id is zero or invalid by setting it to None
        store_id = None if store_id <= 0 else store_id

        try:
            # Create a new User object
            user = User(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                enabled=enabled,
                is_central=is_central,
                store_id=store_id
            )

            # Add the user to the database session
            self.session.add(user)

            # Commit the changes to the database
            self.session.commit()

            # Return the newly created user
            return user

        except pymysql.err.IntegrityError as e:
            # Rollback the transaction if there's a duplicate entry
            self.session.rollback()
            raise ValueError(f"Failed to create user: {str(e)}")

        except Exception as e:
            # Rollback the transaction for any other exceptions
            self.session.rollback()
            raise ValueError(f"An unexpected error occurred: {str(e)}")


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

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter(User.id == user_id).first()

    def assign_store_to_user(self, user_id: int, store_code: str):
        from server.repositories.store_repository import StoreRepository

        user = self.session.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        store = StoreRepository(self.session).get_store_by_code(store_code)

        if not store:
            raise ValueError(f"Store with code {store_code} not found")

        user.store_id = store.id

        try:
            self.session.commit()
            self.session.refresh(user)

        except Exception as e:
            self.session.rollback()
            raise RuntimeError(
                f"An error occurred while assigning store to user: {str(e)}")

        return user

    def search_users_by_store(self, store_code: str):
        # Primero, buscar el store_id usando el store_code
        from server.repositories.store_repository import StoreRepository
        store = StoreRepository(self.session).get_store_by_code(store_code)

        if not store:
            raise ValueError(f"No store found with code: {store_code}")

        # Luego, buscar los usuarios por store_id
        return self.session.query(User).filter(User.store_id == store.id).all()

    def list_users(self): # Obtener todos los usuarios sin aplicar ningún filtro
        return self.session.query(User).all()
