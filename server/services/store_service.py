import grpc
import store_pb2
import store_pb2_grpc
import re
from sqlalchemy.orm import Session
from server.entities.store import Store
from server.entities.base import SessionLocal
from server.repositories.store_repository import StoreRepository
from server.use_cases.create_store import CreateStoreUseCase
from server.use_cases.disable_store import DisableStoreUseCase

class StoreService(store_pb2_grpc.StoreService):
    def __init__(self):
        self.db: Session = SessionLocal()
        self.store_repository = StoreRepository(self.db)
        self.create_store_use_case = CreateStoreUseCase(self.store_repository)
        self.disable_store_use_case = DisableStoreUseCase(self.store_repository)
        
    def CreateStore(self, request: store_pb2.CreateStoreRequest, context: grpc.ServicerContext) -> store_pb2.StoreResponse:
        try:
            
            if not re.match(r"^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{3,50}$", request.code):
                raise ValueError("Store code must contain both letters and numbers, and be between 3 and 50 characters long.")

            
            store = self.create_store_use_case.execute(
                code=request.code,
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
