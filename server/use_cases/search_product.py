from repositories.product_repository   import ProductRepository
from server.entities.product                  import Product
from server.generated.product_pb2             import SearchProductRequest


class SearchProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
  
    def execute(self, unique_code: str = None, name: str = None, size: str = None, color: str = None, enabled: bool = None) -> list[Product]:
        # Llamar al repositorio para buscar productos
        products = self.product_repository.search_product(
            unique_code=unique_code,
            name=name,
            size=size,
            color=color,
            enabled= enabled
        )
        
        return products  # Devolver la lista de productos encontrados

