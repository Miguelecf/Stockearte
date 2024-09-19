import grpc
import product_pb2
import product_pb2_grpc
import re
from sqlalchemy.orm import Session
from server.entities.product import Product
from server.entities.base import SessionLocal
from server.repositories.product_repository import ProductRepository
from server.use_cases.create_product import CreateProductUseCase
from server.use_cases.disable_product import DisableProductUseCase
from server.use_cases.update_product import UpdateProductUseCase

class ProductService(product_pb2_grpc.ProductService):
    def __init__(self):
        self.db: Session        = SessionLocal()
        self.product_repository = ProductRepository(self.db)
        self.create_product_use_case  = CreateProductUseCase(self.product_repository)
        self.disable_product_use_case = DisableProductUseCase(self.product_repository)
        self.update_product_use_case  = UpdateProductUseCase(self.product_repository)
        
    def CreateProduct(self, request: product_pb2.CreateProductRequest, context: grpc.ServicerContext) -> product_pb2.ProductResponse:
        print("service",request)
        try:         
            product = self.create_product_use_case.execute(
                name    	= request.name,
                unique_code = request.unique_code,
                size        = request.size,
                image_url   = request.image_url,
                color       = request.color,
                enabled     = request.enabled
            )
            return product_pb2.ProductResponse(
                name    	= product.name,
                unique_code = product.unique_code,
                size        = product.size,
                image_url   = product.image_url,
                color       = product.color,
                enabled     = product.enabled
            )
            
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return product_pb2.ProductResponse()  # Devuelve ProductResponse vacío
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return product_pb2.ProductResponse()  # Devuelve ProductResponse vacío

    def DisableProduct(self, request: product_pb2.DisableProductRequest, context: grpc.ServicerContext) -> product_pb2.ProductResponse:
        try:
            product = self.disable_product_use_case.execute(
                unique_code = request.unique_code,
                enabled     = request.enabled
            )
            
            return product_pb2.ProductResponse(
                name    	= product.name,
                unique_code = product.unique_code,
                size        = product.size,
                image_url   = product.image_url,
                color       = product.color,
                enabled     = product.enabled
            )
            
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return product_pb2.ProductResponse()  # Consider providing a clearer error message
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return product_pb2.ProductResponse()  # Consider providing a clearer error message
        
    def UpdateProduct(self, unique_code: str, name: str = None, size: str = None, image_url: str = None, color: str = None, enabled: bool = None) -> Product:
        # Validar que el unique_code no esté vacío
        if not unique_code:
            raise ValueError("The unique_code field cannot be empty.")

        # Validar que al menos un campo de actualización haya sido proporcionado
        if all(param is None for param in [name, size, image_url, color, enabled]):
            raise ValueError("At least one field to update must be provided.")

        # Usar el repositorio para obtener el producto y actualizarlo
        updated_product = self.product_repository.update_product(
            unique_code=unique_code,
            name=name,
            size=size,
            image_url=image_url,
            color=color,
            enabled=enabled
        )

        return updated_product
