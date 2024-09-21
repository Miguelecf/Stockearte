from repositories.product_repository import ProductRepository
from server.entities.product import Product
from server.generated.product_pb2 import UpdateProductRequest


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, unique_code: str, name: str = None, size: str = None, image_url: str = None, color: str = None, enabled: bool = None) -> Product:
        return self.product_repository.update_product(name, unique_code, size, image_url, color, enabled)
