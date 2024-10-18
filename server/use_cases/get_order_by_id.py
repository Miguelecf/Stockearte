from repositories.order_repository import OrderRepository
from server.entities.order import Order
from server.entities.order_item import OrderItem
from server.generated.order_pb2 import OrderResponse, OrderItemRequest
from server.entities.order import OrderStatus
from datetime import datetime

class GetOrderByIdUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, order_id: int) -> OrderResponse:
        # Obtener la orden existente a través del ID
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")

        # Crear un objeto OrderResponse para devolver
        order_response = OrderResponse(
            order=order_pb2.Order(
                id=order.id,
                status=order.status,
                observations=order.observations,
                dispatch_order=order.dispatch_order,
                # Si tienes campos adicionales, añádelos aquí
            )
        )

        return order_response
