from server.repositories.store_repository import StoreRepository
from server.entities.store import Store
from generated.store_pb2 import CreateStoreRequest

class CreateStoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository
        
    
    def execute(self, code: str,address: str,city: str,state: str,enabled: bool)-> Store:
        return self.store_repository.create_store(code,address,city,state,enabled)
    