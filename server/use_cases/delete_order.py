from repositories.order_repository import OrderRepository
from server.generated.order_pb2 import DeleteOrderRequest
from google.protobuf.empty_pb2 import Empty

class DeleteOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, request: DeleteOrderRequest) -> Empty:
        # Verificar si la orden existe
        order = self.order_repository.get_order_by_id(request.id)
        if not order:
            raise ValueError(f"Order with ID {request.id} not found")

        # Eliminar la orden
        self.order_repository.delete_order(order.id)
        
        # Devolver una respuesta vacía
        return Empty()
