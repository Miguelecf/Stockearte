from repositories.order_repository import OrderRepository
from server.entities.order import Order
from server.entities.order_item import OrderItem
from server.generated.order_pb2 import CreateOrder, OrderResponse, OrderItemRequest

class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, request) -> OrderResponse:
        # Crear la orden independientemente de los items
        order = self.order_repository.create_order(
            store_id=request.store_id,
            status=request.status.name,
            observations=request.observations,
            dispatch_order=request.dispatch_order,
            request_date=request.request_date.ToDateTime()
        )
        
        # Si hay items en la request, los guarda.
        if request.items:
            order_items = [
                OrderItem(
                    order_id=order.id,
                    item_code=item.item_code,
                    color=item.color,
                    size=item.size,
                    quantity=item.quantity
                )
                for item in request.items
            ]
            self.order_repository.save_order_items(order_items)

        return order