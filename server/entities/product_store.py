from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from server.entities.base import Base  # Asegúrate de que Base esté definida en tu proyecto
from server.entities.product import Product
from server.entities.store import Store

class ProductStore(Base):
    __tablename__ = 'product_store'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)  # Relación con el producto
    store_id = Column(Integer, ForeignKey('store.id'), nullable=False)      # Relación con la tienda
    stock = Column(Integer, nullable=False)  # Cantidad de stock en la tienda

    # Relaciones ORM
    product = relationship('Product', back_populates='product_stores')
    store = relationship('Store', back_populates='product_stores')


