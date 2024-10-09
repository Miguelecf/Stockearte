from repositories.store_repository import StoreRepository
from server.entities.store import Store
from server.generated.store_pb2 import SearchStoreRequest


class SearchStoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    def execute(self, code: str = None, enabled: bool = None) -> list[Store]:
        if enabled is None:
            enabled = False

        stores = self.store_repository.search_store(
            code=code,
            enabled=enabled
        )
        return stores  # Devolver la lista de stores encontrados
