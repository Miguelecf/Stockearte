from repositories.product_repository   import ProductRepository
from server.entities.product                  import Product
from server.generated.product_pb2             import DisableProductRequest

class DisableProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        
    def execute(self, unique_code: str,enabled: bool)-> Product:
        return self.product_repository.disable_product(unique_code,enabled)
    