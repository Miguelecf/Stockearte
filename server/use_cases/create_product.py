from server.repositories.product_repository import ProductRepository
from server.entities.product import Product
from server.generated.product_pb2 import CreateProductRequest
import random
import string


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def generate_unique_code(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase+string.digits, k=10))

    def execute(self, name: str, size: str, image_url: str, color: str, enabled: bool) -> Product:

        unique_code = self.generate_unique_code()

        existing_product = self.product_repository.get_product_by_code(
            unique_code=unique_code)

        while existing_product:
            unique_code = self.generate_unique_code()
            existing_product = self.product_repository.get_product_by_code(
                unique_code=unique_code)

        return self.product_repository.create_product(name, unique_code, size, image_url, color, enabled)
