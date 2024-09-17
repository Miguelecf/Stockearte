from server.entities.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from server.entities.store import Store
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Aquí podrías hashear la contraseña
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    enabled = Column(Boolean, default=True)
    # Relación con Store
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True)
    
    store = relationship("Store", back_populates="users")
