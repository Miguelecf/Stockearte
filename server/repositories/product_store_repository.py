from sqlalchemy.orm import Session
from server.entities.product_store import ProductStore
from server.entities.product import Product  # Asegúrate de que la ruta sea correcta
from server.entities.store import Store  # Asegúrate de que la ruta sea correcta


class ProductStoreRepository:
    def __init__(self, session: Session):
        self.session = session



    def get_product_by_code(self, product_code: str) -> Product:
        """Busca un producto por su código único."""
        return self.db.query(Product).filter(Product.product_code == product_code).first()

    def get_store_by_code(self, store_code: str) -> Store:
        """Busca una tienda por su código único."""
        return self.db.query(Store).filter(Store.store_code == store_code).first()

    #def _validate_stock(self, stock: int) -> None:
    #    """Validates that the stock is a non-negative integer."""
    #    if stock < 0:
    #        raise ValueError("Stock cannot be negative.")

    def assign_stock(self, product_id: int, store_id: int, stock: int) -> ProductStore:
        # Validar que el stock no sea negativo
        #self._validate_stock(stock)

        # Verificar si ya existe una entrada para el mismo producto y tienda
        existing_product_store = self.session.query(ProductStore).filter(
            ProductStore.product_id == product_id,
            ProductStore.store_id == store_id
        ).first()

        if existing_product_store:
            raise ValueError("Stock already assigned for this product and store.")

        # Crear una nueva instancia de ProductStore
        product_store = ProductStore(
            product_id=product_id,
            store_id=store_id,
            stock=stock
        )

        # Añadir la relación producto-tienda a la sesión de la base de datos
        self.session.add(product_store)

        try:
            # Confirmar los cambios en la base de datos
            self.session.commit()
            # Refrescar la instancia para reflejar los datos guardados
            self.session.refresh(product_store)
        except Exception as e:
            # Si ocurre un error, hacer rollback y relanzar la excepción
            self.session.rollback()
            raise RuntimeError(f"An error occurred while assigning stock: {str(e)}")

        # Devolver la relación product-store creada
        return product_store

    def update_stock(self, product_id: int, store_id: int, stock: int) -> ProductStore:
        # Validar que el stock no sea negativo
        #self._validate_stock(stock)

        # Buscar la relación existente entre producto y tienda
        product_store = self.session.query(ProductStore).filter(
            ProductStore.product_id == product_id,
            ProductStore.store_id == store_id
        ).first()

        if not product_store:
            raise ValueError("No stock found for this product and store combination.")

        # Actualizar el stock
        product_store.stock = stock

        try:
            # Confirmar los cambios en la base de datos
            self.session.commit()
            # Refrescar la instancia para reflejar los datos actualizados
            self.session.refresh(product_store)
        except Exception as e:
            # Si ocurre un error, hacer rollback y relanzar la excepción
            self.session.rollback()
            raise RuntimeError(f"An error occurred while updating stock: {str(e)}")

        # Devolver la relación actualizada
        return product_store

    def get_stock(self, product_id: int, store_id: int) -> ProductStore:
        # Buscar el stock de un producto en una tienda
        return self.session.query(ProductStore).filter(
            ProductStore.product_id == product_id,
            ProductStore.store_id == store_id
        ).first()
