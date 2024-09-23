from sqlalchemy.orm import Session
from server.entities.stock_by_store import StockByStore


class StockByStoreRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_stock(self, store_id: int, product_id: int, stock: int) -> StockByStore:
        stock_entry = StockByStore(
            store_id=store_id,
            product_id=product_id,
            stock=stock,
        )

        self.session.add(stock_entry)

        try:
            self.session.commit()
            self.session.refresh(stock_entry)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(
                f"An error occurred while creating the stock entry: {str(e)}"
            )

        return stock_entry

    def get_stock_by_ids(self, store_id: int, product_id: int) -> StockByStore:
        try:
            stock_entry = (
                self.session.query(StockByStore)
                .filter(
                    StockByStore.store_id == store_id,
                    StockByStore.product_id == product_id
                )
                .first()
            )
            return stock_entry
        except Exception as e:
            raise RuntimeError(
                f"Error retrieving stock for store_id {store_id} and product_id {product_id}: {str(e)}"
            )

    def update_stock(self, store_id: int, product_id: int, stock: int) -> StockByStore:
        stock_entry = self.get_stock_by_ids(store_id, product_id)

        if not stock_entry:
            raise ValueError(f"Stock entry not found for store_id {store_id} and product_id {product_id}.")

        stock_entry.stock = stock

        try:
            self.session.commit()
            self.session.refresh(stock_entry)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while updating the stock entry: {str(e)}")

        return stock_entry

    def list_stocks(self):
        try:
            return self.session.query(StockByStore).all()
        except Exception as e:
            raise RuntimeError(f"Error retrieving all stock entries: {str(e)}")

    def delete_stock(self, store_id: int, product_id: int):
        stock_entry = self.get_stock_by_ids(store_id, product_id)

        if not stock_entry:
            raise ValueError(f"Stock entry not found for store_id {store_id} and product_id {product_id}.")

        self.session.delete(stock_entry)

        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while deleting the stock entry: {str(e)}")
