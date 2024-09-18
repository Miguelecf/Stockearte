# store.py
from server.entities.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=True)
    
    # Use string-based references for relationships to avoid circular imports
    # stocks = relationship("StockByStore", back_populates="store")
    users = relationship("User", back_populates="store")
