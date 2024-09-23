from repositories.stock_by_store_repository import StockByStoreRepository
from server.entities.stock_by_store import StockByStore


class SearchStockByStoreUseCase:
    def __init__(self, stock_by_store_repository: StockByStoreRepository):
        self.stock_by_store_repository = stock_by_store_repository

    def execute(self, store_id: int, product_id: int = None) -> list[StockByStore]:
        """
        Busca el stock por tienda. Si se proporciona un `product_id`, busca el stock de ese producto específico en la tienda.
        """
        return self.stock_by_store_repository.search_stock_by_store(store_id, product_id)
