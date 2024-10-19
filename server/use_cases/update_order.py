from repositories.order_repository import OrderRepository
from server.entities.order import Order
from server.generated.order_pb2 import UpdateOrderRequest, OrderResponse

class UpdateOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, request: UpdateOrderRequest) -> OrderResponse:
        # Obtener la orden existente
        order = self.order_repository.get_order_by_id(request.id)
        if not order:
            raise ValueError(f"Order with ID {request.id} not found")

        # Actualizar los campos de la orden
        order.status = request.status.name
        order.observations = request.observations
        order.dispatch_order = request.dispatch_order

        # Guardar la orden actualizada
        updated_order = self.order_repository.update_order(order)

        return updated_order
