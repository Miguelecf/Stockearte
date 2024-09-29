from typing import List  # Importa List de typing
from repositories.user_repository import UserRepository
from repositories.store_repository import StoreRepository  # Mueve la importación aquí
from server.entities.user import User

class SearchUserByStoreUseCase:
    def __init__(self, user_repository: UserRepository, store_repository: StoreRepository):
        self.user_repository = user_repository
        self.store_repository = store_repository

    def execute(self, store_code: str) -> list[User]:  # Usa List aquí
        # Obtener el store_id usando el store_code
        users = self.user_repository.search_users_by_store(
            store_code = store_code
        )

        return users
