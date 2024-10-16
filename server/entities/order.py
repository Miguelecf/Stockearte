#order.py
from server.entities.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum

class OrderStatus(enum.Enum):
    SOLICITADA = 1
    ACEPTADA = 2
    RECHAZADA = 3
    RECIBIDA = 4
    
class Order(Base):
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key= True, index= True)
    status = Column(Enum(OrderStatus), index = True, nullable = False)
    observations = Column(Text, nullable= True)
    dispatch_order = Column(String(50), nullable= True)
    request_date = Column(DateTime, nullable = False)
    received_date = Column(DateTime, nullable= True)
    store_id = Column(Integer, ForeignKey('stores.id'),nullable= False)
    items = relationship("OrderItem", back_populates= "order")
    