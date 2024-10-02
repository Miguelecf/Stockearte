import grpc 
from generated import product_store_pb2
from generated import product_pb2_grpc

import re
from sqlalchemy.orm import Session
from server.entities.product import Product
from server.entities.base import SessionLocal
from server.generated import product_store_pb2_grpc
from server.repositories.product_store_repository import ProductStoreRepository
from server.use_cases.create_product_store import CreateProductStoreUseCase


class ProductStoreService(product_store_pb2_grpc.ProductStoreService):
    
    def __init__(self):
        # Iniciar una sesión de la base de datos
        self.db: Session = SessionLocal()
        self.product_store_repository = ProductStoreRepository(self.db)
        self.create_product_store_use_case = CreateProductStoreUseCase(self.product_store_repository)
    
    def CreateProductStore(self, request, context):
        try:
            # Llamar al caso de uso para crear la relación ProductStore
            product_store = self.create_product_store_use_case.execute(request)

            # Devolver la respuesta de gRPC en formato ProductStore
            return product_store_pb2.ProductStore(
                id=product_store.id,
                store_id=product_store.store_id,
                product_id=product_store.product_id,
                stock=product_store.stock,
                enabled=product_store.enabled
            )
        
        except Exception as e:
            # En caso de error, devolver una respuesta con un error de contexto gRPC
            context.set_details(f"Error while creating ProductStore: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return product_store_pb2.ProductStore()
    
    def __del__(self):
        # Cerrar la sesión de la base de datos cuando se destruya la instancia
        self.db.close()