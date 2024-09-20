from server.entities.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Text


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    unique_code = Column(String(10), unique=True, nullable=False)  # Código generado aleatoriamente
    size = Column(String(10), nullable=False)
    image_url = Column(String(255), nullable=True)  # Ruta o URL de la imagen del producto
    color = Column(String(50), nullable=False)
    enabled = Column(Boolean, default=True)
    # Relación con StockByStore
    #stocks = relationship("StockByStore", back_populates="products")
