from repositories.stock_by_store_repository import StockByStoreRepository
from server.entities.stock_by_store import StockByStore


class UpdateStockByStoreUseCase:
    def __init__(self, stock_by_store_repository: StockByStoreRepository):
        self.stock_by_store_repository = stock_by_store_repository

    def execute(self, store_id: int, product_id: int, stock: int) -> StockByStore:
        """
        Actualiza el stock para un producto específico en una tienda.
        
        :param store_id: El ID de la tienda donde se actualizará el stock.
        :param product_id: El ID del producto cuyo stock se actualizará.
        :param stock: La nueva cantidad de stock.
        :return: La entidad actualizada `StockByStore`.
        """
        return self.stock_by_store_repository.update_stock_by_store(store_id, product_id, stock)
