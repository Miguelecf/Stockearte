from server.entities.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from server.entities.product import Product
from sqlalchemy.orm import relationship


class StockByStore(Base):
    __tablename__ = "stock_by_store"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    color = Column(String(50), nullable=False)
    size = Column(String(10), nullable=False)
    stock = Column(Integer, default=0)  # Stock inicial a 0
    
    # Relación con Store y Product
    store = relationship("Store", back_populates="stocks")
    product = relationship("Product", back_populates="stocks")
