from server.repositories.stock_by_store_repository import StockByStoreRepository
from server.entities.stock_by_store import StockByStore

class AssignStockByStoreUseCase:
    def __init__(self, stock_by_store_repository: StockByStoreRepository):
        self.stock_by_store_repository = stock_by_store_repository

    def execute(self, store_id: int, product_id: int, stock: int) -> StockByStore:
        print(f"Assigning stock for store {store_id} and product {product_id} with stock {stock}")
        return self.stock_by_store_repository.create_stock_by_store(store_id, product_id, stock)
