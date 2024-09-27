import grpc
from generated import store_pb2
from generated import store_pb2_grpc
import re
from sqlalchemy.orm import Session
from server.entities.store import Store
from server.entities.base import SessionLocal
from repositories.store_repository  import StoreRepository
from server.use_cases.create_store  import CreateStoreUseCase
from server.use_cases.disable_store import DisableStoreUseCase
from server.use_cases.search_store  import SearchStoreUseCase

class StoreService(store_pb2_grpc.StoreService):
    def __init__(self):
        self.db: Session = SessionLocal()
        self.store_repository = StoreRepository(self.db)
        self.create_store_use_case = CreateStoreUseCase(self.store_repository)
        self.disable_store_use_case = DisableStoreUseCase(self.store_repository)
        self.search_store_use_case = SearchStoreUseCase(self.store_repository)
        
    def CreateStore(self, request: store_pb2.CreateStoreRequest, context: grpc.ServicerContext) -> store_pb2.StoreResponse:
        try:
            
            if not re.match(r"^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{3,50}$", request.code):
                raise ValueError("Store code must contain both letters and numbers, and be between 3 and 50 characters long.")

            
            store = self.create_store_use_case.execute(
                code=request.code, #TODO: que no tenga espacios cuando ingrese.
                address=request.address,
                city=request.city,
                state=request.state,
                enabled=request.enabled
            )
            return store_pb2.StoreResponse(
                code=store.code,
                address=store.address,
                city=store.city,
                state=store.state,
                enabled=store.enabled
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return store_pb2.StoreResponse()  # Devuelve StoreResponse vacío
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return store_pb2.StoreResponse()  # Devuelve StoreResponse vacío

        
    def DisableStore(self, request: store_pb2.DisableStoreRequest, context: grpc.ServicerContext) -> store_pb2.StoreResponse:
        try:
            store = self.disable_store_use_case.execute(
                code=request.code,
                enabled=request.enabled
            )
            return store_pb2.StoreResponse(
                code=store.code,
                address=store.address,
                city=store.city,
                state=store.state,
                enabled=store.enabled
            )
        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return store_pb2.StoreResponse()  # Consider providing a clearer error message
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return store_pb2.StoreResponse()  # Consider providing a clearer error message

    def SearchStore(self, request, context) -> store_pb2.SearchStoreResponse:
        print("storeservice 1 " ,request)
        # Extraer parámetros de búsqueda del request
        code    = request.code if request.code else None
        enabled = request.enabled if request.enabled else None
        #enabled = request.enabled if request.enabled is not None else None

        # Validar que al menos un parámetro de búsqueda haya sido proporcionado
        if all (param is none for param in [code, enabled]):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          "At least one search parameter must be provided.")

        # Llamar al repositorio para buscar tiendas
        found_stores = self.store_repository.search_store(
            code    = code,
            enabled = enabled
        )

        # Mapear las tiendas encontradas a la respuesta gRPC
        response = store_pb2.SearchStoreResponse()
        for store in found_stores:
            store_response          = response.stores.add()
            store_response.id       = store.id
            store_response.code     = store.code
            store_response.address  = store.address
            store_response.city     = store.city
            store_response.state    = store.state
            store_response.enabled  = store.enabled
        print("storeservice 2 " ,response)
        return response

