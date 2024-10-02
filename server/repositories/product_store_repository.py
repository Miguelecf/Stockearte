from sqlalchemy.orm import Session, Query
from server.entities.product_store import ProductStore
from server.entities.store import Store
from server.entities.product import Product

class ProductStoreRepository:
    
    def __init__(self,session: Session):
        self.session = session
        
    
    def create_product_store(self, store_code: str, product_code: str, stock: int, enabled: bool) -> ProductStore:
        # Buscar la tienda por su código
        store = self.session.query(Store).filter(Store.code == store_code).first()
        if not store:
            raise ValueError(f"Store with code {store_code} not found")

        # Buscar el producto por su unique_code
        product = self.session.query(Product).filter(Product.unique_code == product_code).first()
        if not product:
            raise ValueError(f"Product with unique code {product_code} not found")

        # Crear la relación ProductStore usando los IDs obtenidos
        product_store = ProductStore(
            store_id=store.id,  # Usamos el ID de la tienda
            product_id=product.id,  # Usamos el ID del producto
            stock=stock,
            enabled=enabled
        )

        # Añadir y guardar en la base de datos
        self.session.add(product_store)

        try:
            self.session.commit()
            self.session.refresh(product_store)

        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while creating the product_store: {str(e)}")

        return product_store
            
        