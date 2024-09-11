# domain/interfaces.py
from typing import Optional
from domain.entities import User

class UserRepositoryInterface:
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Devuelve un usuario basado en el nombre de usuario."""
        raise NotImplementedError