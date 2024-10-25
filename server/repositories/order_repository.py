#order_repository.py
from sqlalchemy.orm import Session, Query
from server.entities.order import Order , OrderStatus
from server.entities.order_item import OrderItem
from typing import List
from datetime import datetime
from server.entities.order import Order, OrderStatus
from server.entities.order_item import OrderItem
from datetime import datetime

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session 
        
    

    def create_order(
    self,
    store_id: int,
    status: str,
    observations: str,
    dispatch_order: str,
    request_date: datetime,
    items: list[OrderItem] = None  # Aceptar una lista de items opcionalmente
) -> Order:
    # Crea la instancia de la orden usando los valores proporcionados
        order = Order(
        store_id=store_id,
        status=OrderStatus.SOLICITADA,
        observations=observations,
        dispatch_order=dispatch_order,
        request_date=request_date,
    )
        self.session.add(order)

        try:
            # Intentar guardar la orden en la base de datos
            self.session.commit()
            self.session.refresh(order)  # Refresca para obtener la información más reciente de la DB

            # Guardar los OrderItems si se proporcionan
            if items:
                for item in items:
                    item.order_id = order.id  # Asegurar que cada item tenga el ID de la orden
                    self.session.add(item)
                
                # Guardar los items en la base de datos
                self.session.commit()

        except Exception as e:
            self.session.rollback()  # Revertir la transacción en caso de error
            raise RuntimeError(f"An error occurred while creating the order and its items: {str(e)}")

        return order



    def get_order_by_id(self, order_id: int) -> Order:
        try:
            order = self.session.query(Order).filter(Order.id == order_id).first()
            return order
        except Exception as e:
            raise RuntimeError(f"Error retrieving order by ID {order_id}: {str(e)}")

    def list_orders(self) -> List[Order]:
        try:
            return self.session.query(Order).all()
        except Exception as e:
            raise RuntimeError(f"Error listing orders: {str(e)}")
        
    def update_order(
        self,
        order_id: int,
        status: str = None,
        observations: str = None,
        dispatch_order: str = None,
        received_date=None,
    ) -> Order:
        
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found.")

        if status not in [None, ""]:
            order.status = OrderStatus[status]  # Esto convierte un string al enum correspondiente

        if observations not in [None, ""]:
            order.observations = observations
        if dispatch_order not in [None, ""]:
            order.dispatch_order = dispatch_order
        if received_date is not None:
            order.received_date = received_date

        try:
            self.session.commit()
            self.session.refresh(order)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while updating the order with ID {order_id}: {str(e)}")

        return order
    
    def save_order_items(self, order_items: List[OrderItem]) -> None:
        self.session.add_all(order_items)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while saving order items: {str(e)}")

    def delete_order_items_by_order_id(self, order_id: int) -> None:
        try:
            self.session.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while deleting order items for order ID {order_id}: {str(e)}")