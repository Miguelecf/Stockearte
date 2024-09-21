import grpc
# import product_pb2
# import product_pb2_grpc

from generated import product_pb2
from generated import product_pb2_grpc

import re
from sqlalchemy.orm import Session
from server.entities.product import Product
from server.entities.base import SessionLocal
from server.repositories.product_repository import ProductRepository
from server.use_cases.create_product import CreateProductUseCase
from server.use_cases.disable_product import DisableProductUseCase
from server.use_cases.update_product import UpdateProductUseCase
from server.use_cases.search_product import SearchProductUseCase
# from server.use_cases.search_product import P


class ProductService(product_pb2_grpc.ProductService):
    def __init__(self):
        self.db: Session = SessionLocal()
        self.product_repository = ProductRepository(self.db)
        self.create_product_use_case = CreateProductUseCase(
            self.product_repository)
        self.disable_product_use_case = DisableProductUseCase(
            self.product_repository)
        self.update_product_use_case = UpdateProductUseCase(
            self.product_repository)
        self.search_product_use_case = SearchProductUseCase(
            self.product_repository)

    def CreateProduct(self, request: product_pb2.CreateProductRequest, context: grpc.ServicerContext) -> product_pb2.ProductResponse:
        try:
            product = self.create_product_use_case.execute(
                name=request.name,
                unique_code=request.unique_code,
                size=request.size,
                image_url=request.image_url,
                color=request.color,
                enabled=request.enabled
            )
            return product_pb2.ProductResponse(
                name=product.name,
                unique_code=product.unique_code,
                size=product.size,
                image_url=product.image_url,
                color=product.color,
                enabled=product.enabled
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
                unique_code=request.unique_code,
                enabled=request.enabled
            )

            return product_pb2.ProductResponse(
                name=product.name,
                unique_code=product.unique_code,
                size=product.size,
                image_url=product.image_url,
                color=product.color,
                enabled=product.enabled
            )

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            # Consider providing a clearer error message
            return product_pb2.ProductResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            # Consider providing a clearer error message
            return product_pb2.ProductResponse()

    def UpdateProduct(self, request: product_pb2.UpdateProductRequest, context: grpc.ServicerContext) -> product_pb2.ProductResponse:
        # Validar que el unique_code no esté vacío
        unique_code = request.unique_code
        if not unique_code:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("The unique_code field cannot be empty.")
            return product_pb2.ProductResponse()  # Devuelve ProductResponse vacío

        # Validar que al menos un campo de actualización haya sido proporcionado
        if all(param is None for param in [request.name, request.size, request.image_url, request.color]):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(
                "At least one field to update must be provided.")
            return product_pb2.ProductResponse()  # Devuelve ProductResponse vacío

        try:
            # Usar el repositorio para actualizar el producto
            updated_product = self.product_repository.update_product(
                unique_code=unique_code,
                name=request.name,
                size=request.size,
                image_url=request.image_url,
                color=request.color,
                enabled=request.enabled
            )

            return product_pb2.ProductResponse(
                name=updated_product.name,
                unique_code=updated_product.unique_code,
                size=updated_product.size,
                image_url=updated_product.image_url,
                color=updated_product.color,
                enabled=updated_product.enabled
            )

        except ValueError as ve:
            print(f"Validation error: {str(ve)}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(ve))
            return product_pb2.ProductResponse()  # Devuelve ProductResponse vacío

        except Exception as e:
            print(f"Unexpected error during product update: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(
                f"An error occurred while updating the product: {str(e)}")
            return product_pb2.ProductResponse()  # Devuelve ProductResponse vacío

    def SearchProduct(self, request, context) -> product_pb2.ProductListResponse:
        # Extraer parámetros de búsqueda del request
        name = request.name if request.name else None
        unique_code = request.unique_code if request.unique_code else None
        size = request.size if request.size else None
        color = request.color if request.color else None

        # Validar que al menos un parámetro de búsqueda haya sido proporcionado
        if all(param is None for param in [name, unique_code, size, color]):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          "At least one search parameter must be provided.")

        # Llamar al repositorio para buscar productos
        found_products = self.product_repository.search_product(
            name=name,
            unique_code=unique_code,
            size=size,
            color=color
        )

        # Mapear los productos encontrados a la respuesta gRPC
        response = product_pb2.ProductListResponse()
        for product in found_products:
            product_response = response.products.add()
            product_response.name = product.name
            product_response.size = product.size
            product_response.color = product.color
            product_response.unique_code = product.unique_code
            product_response.image_url = product.image_url
            product_response.enabled = product.enabled

        return response
