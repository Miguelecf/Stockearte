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
#from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from my_kafka.kafka_producer import send_order_to_kafka
from server.repositories.store_repository import StoreRepository

class OrderService(order_pb2_grpc.OrderService):
    
    
    def __init__(self):
        # Iniciar una sesión de la base de datos
        self.db: Session = SessionLocal()
        self.order_repository = OrderRepository(self.db)
        self.create_order_use_case = CreateOrderUseCase(self.order_repository)
        self.add_order_items_use_case = AddOrderItemsUseCase(self.order_repository)
        self.store_repository = StoreRepository(self.db)

    def CreateOrder(self, request, context):
        print("Received request:", request)  
        try:
            # Ejecutar la creación de la orden
            order = self.create_order_use_case.execute(request)
            
            # Crear el timestamp para la fecha de solicitud
            request_date = Timestamp()
            request_date.GetCurrentTime()  # Obtener tiempo actual

            # Verificar y establecer la fecha de recepción
            received_date = Timestamp()
            if order.received_date:
                received_date.FromDatetime(order.received_date)
            else:
                received_date = None  # Asegúrate de que sea None si no hay fecha

            # Llama a la función para enviar el mensaje a Kafka
            store = self.store_repository.get_store_by_id(order.store_id)
            store_code = store.code
            
            if not store_code:
                raise ValueError("Store code not found.")

            send_order_to_kafka(
                store_code=store_code,  # Código de la tienda
                order_id=order.id,  # ID de la orden
                items=[{
                    "id": item.id,
                    "order_id": item.order_id,
                    "item_code": item.item_code,
                    "color": item.color,
                    "size": item.size,
                    "quantity": item.quantity
                } for item in order.items],  # Lista de ítems
                request_date=request_date.ToDatetime().isoformat()  # Convertir el timestamp a formato ISO
            )

            # Retorna la respuesta de la orden
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
            # Validar el request aquí si es necesario
            
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

        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return order_pb2.Order()
        except Exception as e:
            context.set_details(f"Error while adding order items: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return order_pb2.Order()

    def __del__(self):
        # Cerrar la sesión de la base de datos cuando se destruya la instancia
        self.db.close()
