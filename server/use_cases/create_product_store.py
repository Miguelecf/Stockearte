from server.repositories.product_store_repository import ProductStoreRepository
from server.entities.product_store import ProductStore
from server.generated.product_store_pb2 import CreateProductStoreRequest



class CreateProductStoreUseCase:
    def __init__(self, product_store_repository: ProductStoreRepository):
        self.product_store_repository = product_store_repository
        
    
    def execute(self, request: CreateProductStoreRequest) -> ProductStore:
        # Extraer los datos del request
        store_code = request.store_code
        product_code = request.product_code
        stock = request.stock
        enabled = request.enabled

        # Crear el ProductStore usando el repositorio
        product_store = self.product_store_repository.create_product_store(
            store_code=store_code,
            product_code=product_code,
            stock=stock,
            enabled=enabled
        )

        return product_store