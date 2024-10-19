from server.entities.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key= True, index= True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable= False)
    item_code = Column(String(50), nullable= False)
    color = Column(String(50), nullable= False)
    size = Column(String(50), nullable= False)
    quantity = Column(Integer, nullable= False)
    order = relationship("Order",back_populates="items")
    