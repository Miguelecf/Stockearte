from repositories.order_repository import OrderRepository
from server.entities.order import Order
from server.entities.order_item import OrderItem
from server.generated.order_pb2 import OrderResponse, OrderItemRequest

class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def execute(self, request) -> OrderResponse:
        if not request.store_id:
            raise ValueError("store_id es requerido.")
        
        if not request.observations:
            raise ValueError("observations es requerido.")

        # Verifica que el estado sea válido
        if request.status is None or request.status not in OrderStatus:
            raise ValueError("status es inválido.")

        # Verifica que request_date se pueda convertir
        try:
            request_date = request.request_date.ToDateTime()
        except Exception as e:
            raise ValueError(f"Error al convertir request_date: {str(e)}")
        
        # Crear la orden independientemente de los items
        order = self.order_repository.create_order(
            store_id=request.store_id,
            status=request.status.name,
            observations=request.observations,
            dispatch_order=request.dispatch_order,
            request_date=request_date
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
