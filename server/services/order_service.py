import grpc
from generated import order_pb2
from generated import order_pb2_grpc
from sqlalchemy.orm import Session
from server.entities.order import Order
from server.entities.order_item import OrderItem
from server.entities.base import SessionLocal
from server.repositories.order_repository import OrderRepository
from server.use_cases.create_order import CreateOrderUseCase
from server.use_cases.add_order_items import AddOrderItemsUseCase

class OrderService(order_pb2_grpc.OrderService):
    
    def __init__(self):
        # Iniciar una sesión de la base de datos
        self.db: Session = SessionLocal()
        self.order_repository = OrderRepository(self.db)
        self.create_order_use_case = CreateOrderUseCase(self.order_repository)
        self.add_order_items_use_case = AddOrderItemsUseCase(self.order_repository)

    def CreateOrder(self, request, context):
        try:
            # Llamar al caso de uso para crear la orden
            order = self.create_order_use_case.execute(request)

            # Devolver la respuesta de gRPC en formato Order
            return order_pb2.Order(
                id=order.id,
                status=order.status,
                observations=order.observations,
                dispatch_order=order.dispatch_order,
                request_date=order.request_date,
                received_date=order.received_date,
                store_id=order.store_id,
                items=[order_pb2.OrderItem(
                    id=item.id,
                    order_id=item.order_id,
                    item_code=item.item_code,
                    color=item.color,
                    size=item.size,
                    quantity=item.quantity
                ) for item in order.items]
            )
        
        except Exception as e:
            # En caso de error, devolver una respuesta con un error de contexto gRPC
            context.set_details(f"Error while creating order: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_pb2.Order()

    def AddOrderItems(self, request, context):
        try:
            # Llamar al caso de uso para agregar los ítems a la orden
            order = self.add_order_items_use_case.execute(request)

            # Devolver la respuesta de gRPC en formato Order
            return order_pb2.Order(
                id=order.id,
                status=order.status,
                observations=order.observations,
                dispatch_order=order.dispatch_order,
                request_date=order.request_date,
                received_date=order.received_date,
                store_id=order.store_id,
                items=[order_pb2.OrderItem(
                    id=item.id,
                    order_id=item.order_id,
                    item_code=item.item_code,
                    color=item.color,
                    size=item.size,
                    quantity=item.quantity
                ) for item in order.items]
            )

        except Exception as e:
            # En caso de error, devolver una respuesta con un error de contexto gRPC
            context.set_details(f"Error while adding order items: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_pb2.Order()

    def __del__(self):
        # Cerrar la sesión de la base de datos cuando se destruya la instancia
        self.db.close()
