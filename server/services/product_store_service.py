import grpc
from generated import product_store_pb2
from generated import product_store_pb2_grpc
from sqlalchemy.orm import Session
from server.entities.base import SessionLocal
from repositories.product_store_repository import ProductStoreRepository
from server.use_cases.create_product_store import CreateProductStoreUseCase
from server.use_cases.update_product_store import UpdateProductStoreUseCase
from server.use_cases.search_product_store import SearchProductStoreUseCase  # Asegúrate de que esto esté implementado

class ProductStoreService(product_store_pb2_grpc.ProductStoreServiceServicer):
    def __init__(self):
        self.db: Session = SessionLocal()
        self.product_store_repository = ProductStoreRepository(self.db)
        self.create_product_store_use_case = CreateProductStoreUseCase(self.product_store_repository)
        self.update_product_store_use_case = UpdateProductStoreUseCase(self.product_store_repository)
        self.search_product_store_use_case = SearchProductStoreUseCase(self.product_store_repository)
        
    def CreateProductStore(self, request: product_store_pb2.CreateProductStoreRequest, context: grpc.ServicerContext) -> product_store_pb2.ProductStoreResponse:
        try:
            # Verificar que el producto y la tienda existen usando los códigos en lugar de los IDs
            product_exists = self.product_store_repository.get_product_by_code(request.product_code)
            store_exists = self.product_store_repository.get_store_by_code(request.store_code)

            if not product_exists:
                raise ValueError("Product does not exist.")
            if not store_exists:
                raise ValueError("Store does not exist.")

            # Si ambos existen, crear la relación producto-tienda
            product_store = self.create_product_store_use_case.execute(
                product_code=request.product_code,  # Usar el código del producto
                store_code=request.store_code,  # Usar el código de la tienda
                stock=request.stock
            )
            return product_store_pb2.ProductStoreResponse(
                product_code=product_store.product_code,
                store_code=product_store.store_code,
                stock=product_store.stock
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return product_store_pb2.ProductStoreResponse() 
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return product_store_pb2.ProductStoreResponse()


    def UpdateProductStore(self, request: product_store_pb2.UpdateProductStoreRequest, context: grpc.ServicerContext) -> product_store_pb2.ProductStoreResponse:
        try:
            # Ejecutar el caso de uso para actualizar el stock en la tienda
            product_store = self.update_product_store_use_case.execute(
                product_code=request.product_code,
                store_code=request.store_code,
                stock=request.stock
            )
            return product_store_pb2.ProductStoreResponse(
                product_code=product_store.product_code,
                store_code=product_store.store_code,
                stock=product_store.stock
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return product_store_pb2.ProductStoreResponse()  # Devuelve ProductStoreResponse vacío
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return product_store_pb2.ProductStoreResponse()  # Devuelve ProductStoreResponse vacío

    def SearchProductStore(self, request: product_store_pb2.SarchProductStoreRequest, context: grpc.ServicerContext) -> product_store_pb2.ProductStoreResponse:
        try:
            # Ejecutar el caso de uso para obtener la relación producto-tienda
            product_store = self.search_product_store_use_case.execute(
                product_code=request.product_code,
                store_code=request.store_code
            )
            
            if product_store:
                return product_store_pb2.ProductStoreResponse(
                    product_code=product_store.product_code,
                    store_code=product_store.store_code,
                    stock=product_store.stock
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Product store relationship not found")
                return product_store_pb2.ProductStoreResponse() 

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return product_store_pb2.ProductStoreResponse() 
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return product_store_pb2.ProductStoreResponse() 
