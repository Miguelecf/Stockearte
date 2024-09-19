from repositories.store_repository import StoreRepository
from server.entities.store import Store
from server.generated.store_pb2 import DisableStoreRequest

class DisableStoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository
        
    def execute(self,code: str,enabled: bool)-> Store:
        return self.store_repository.disable_store(code,enabled)
    