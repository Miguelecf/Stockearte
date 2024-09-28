from repositories.product_store_repository import ProductStoreRepository
from server.entities.product_store import ProductStore

class CreateProductStoreUseCase:
    def __init__(self, product_store_repository: ProductStoreRepository):
        self.product_store_repository = product_store_repository

    def execute(self, product_code: str, store_code: str, stock: int) -> ProductStore:
        # Obtener el ID del producto y de la tienda usando los códigos
        product = self.product_store_repository.get_product_by_code(product_code)
        store = self.product_store_repository.get_store_by_code(store_code)

        if not product or not store:
            raise ValueError("Product or Store does not exist.")

        # Asignar stock
        return self.product_store_repository.assign_stock(
            product_id=product.id, 
            store_id=store.id, 
            stock=stock
        )
