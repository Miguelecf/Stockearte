from server.repositories.product_repository import ProductRepository
from server.entities.product                import Product
from server.generated.product_pb2           import CreateProductRequest

class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, name: str,unique_code: str,size: str, image_url: str, color: str, enabled: bool)-> Product:
        return self.product_repository.create_product(name,unique_code,size,image_url,color,enabled)