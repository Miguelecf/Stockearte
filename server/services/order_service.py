import grpc
from generated import order_pb2
from generated import order_pb2_grpc
from sqlalchemy.orm import Session
from server.entities.order import Order, OrderStatus
from server.entities.order_item import OrderItem
from server.entities.base import SessionLocal
from server.repositories.order_repository import OrderRepository
from server.use_cases.create_order import CreateOrderUseCase
from server.use_cases.add_order_items import AddOrderItemsUseCase
from server.use_cases.get_order_by_id import GetOrderByIdUseCase


from google.protobuf.timestamp_pb2 import Timestamp
class OrderService(order_pb2_grpc.OrderService):
    
    def __init__(self):
        # Iniciar una sesión de la base de datos
        self.db: Session = SessionLocal()
        self.order_repository = OrderRepository(self.db)
        self.create_order_use_case = CreateOrderUseCase(self.order_repository)
        self.add_order_items_use_case = AddOrderItemsUseCase(self.order_repository)

    def CreateOrder(self, request, context):
        print("Received request:", request)  
        try:
            order = self.create_order_use_case.execute(request)
            
            # Crear Timestamps
            request_date = Timestamp()
            request_date.GetCurrentTime()  # Obtener tiempo actual

            received_date = Timestamp()
            if order.received_date:
                received_date.FromDatetime(order.received_date)

            return order_pb2.OrderResponse(
                order=order_pb2.Order(
                    id=order.id,
                    status=OrderStatus.SOLICITADA.value,
                    observations=order.observations,
                    dispatch_order=order.dispatch_order,
                    request_date=request_date,
                    received_date=received_date,
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
            )
        
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return order_pb2.OrderResponse()  # Retorna un objeto vacío en caso de error

        except Exception as e:
            context.set_details(f"Error while creating order: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_pb2.OrderResponse()


    def AddOrderItems(self, request, context):
        try:
            order = self.add_order_items_use_case.execute(request)

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

        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return order_pb2.Order()
        except Exception as e:
            context.set_details(f"Error while adding order items: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_pb2.Order()

    def UpdateOrder(self, request, context):
        print("Received request to update order: ", request)
        try:
            # Obtener la orden existente a través del ID
            order = self.get_order_by_id.execute(request.id)

            if not order:
                context.set_details(f"Order with ID {request.id} not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return order_pb2.OrderResponse()

            # Actualizar los campos solo si están presentes en el request
            if request.HasField('status'):
                order.status = OrderStatus(request.status).value

            if request.HasField('observations'):
                order.observations = request.observations

            if request.HasField('dispatch_order'):
                order.dispatch_order = request.dispatch_order

            if request.HasField('store_id'):
                order.store_id = request.store_id

            if request.items:
                order.items = [
                    self.update_order_item_use_case.execute(item) for item in request.items
                ]

            # Guardar los cambios
            updated_order = self.update_order_use_case.execute(order)

            # Crear Timestamps
            request_date = Timestamp()
            request_date.FromDatetime(updated_order.request_date)

            received_date = Timestamp()
            if updated_order.received_date:
                received_date.FromDatetime(updated_order.received_date)

            return order_pb2.OrderResponse(
                order=order_pb2.Order(
                    id=updated_order.id,
                    status=updated_order.status,
                    observations=updated_order.observations,
                    dispatch_order=updated_order.dispatch_order,
                    request_date=request_date,
                    received_date=received_date,
                    store_id=updated_order.store_id,
                    items=[order_pb2.OrderItem(
                        id=item.id,
                        order_id=item.order_id,
                        item_code=item.item_code,
                        color=item.color,
                        size=item.size,
                        quantity=item.quantity
                    ) for item in updated_order.items]
                )
            )
        
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return order_pb2.OrderResponse()  # Retorna un objeto vacío en caso de error

        except Exception as e:
            context.set_details(f"Error while updating order: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_pb2.OrderResponse()

    def get_order_by_id(self, order_id: int) -> Order:
        order = self.session.query(Order).filter(Order.id == order_id).first()  # Busca la orden por ID

        if not order:
            raise ValueError(f"Order with ID {order_id} not found.")  # Lanza un error si no se encuentra la orden

        return order  # Devuelve el objeto Order si se encuentra
    
    def __del__(self):
        # Cerrar la sesión de la base de datos cuando se destruya la instancia
        self.db.close()
