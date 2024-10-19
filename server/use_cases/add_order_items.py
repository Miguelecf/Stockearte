from repositories.order_repository import OrderRepository
from server.entities.order import Order
from server.entities.order_item import OrderItem
from server.generated.order_pb2 import OrderRequest, OrderResponse, OrderItemRequest


class AddOrderItemsUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: int, items: list[OrderItemRequest]):
        # Convertir los `OrderItemRequest` a `OrderItem` y asignarles el `order_id`.
        order_items = [
            OrderItem(
                order_id=order_id,
                item_code=item.item_code,
                color=item.color,
                size=item.size,
                quantity=item.quantity
            )
            for item in items
        ]
        
        self.order_repository.save_order_items(order_items)
