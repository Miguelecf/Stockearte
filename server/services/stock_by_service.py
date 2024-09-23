import grpc
from generated import stock_by_store_pb2  # Debes generar el archivo .proto correspondiente
from generated import stock_by_store_pb2_grpc

from sqlalchemy.orm import Session
from server.entities.stock_by_store import StockByStore
from server.entities.base import SessionLocal
from server.repositories.stock_by_store_repository import StockByStoreRepository
from server.use_cases.assign_stock_by_store import CreateStockByStoreUseCase
from server.use_cases.update_stock_by_store import UpdateStockByStoreUseCase
from server.use_cases.search_stock_by_store import SearchStockByStoreUseCase


class StockByStoreService(stock_by_store_pb2_grpc.StockByStoreServiceServicer):
    def __init__(self):
        self.db: Session = SessionLocal()
        self.stock_by_store_repository = StockByStoreRepository(self.db)
        self.create_stock_by_store_use_case = CreateStockByStoreUseCase(self.stock_by_store_repository)
        self.update_stock_by_store_use_case = UpdateStockByStoreUseCase(self.stock_by_store_repository)
        self.search_stock_by_store_use_case = SearchStockByStoreUseCase(self.stock_by_store_repository)

        
    def AssignStockByStore(self, request: stock_by_store_pb2.AssignStockRequest, context: grpc.ServicerContext) -> stock_by_store_pb2.StockByStoreResponse:
        try:
            stock_record = self.assign_stock_use_case.execute(
                store_id=request.store_id,
                product_id=request.product_id,
                stock=request.stock
            )

            return stock_by_store_pb2.StockByStoreResponse(
                store_id=stock_record.store_id,
                product_id=stock_record.product_id,
                stock=stock_record.stock
            )

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return stock_by_store_pb2.StockByStoreResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return stock_by_store_pb2.StockByStoreResponse()
        


    def UpdateStockByStore(self, request: stock_by_store_pb2.UpdateStockByStoreRequest, context: grpc.ServicerContext) -> stock_by_store_pb2.StockByStoreResponse:
        try:
            stock_by_store = self.update_stock_by_store_use_case.execute(
                store_id=request.store_id,
                product_id=request.product_id,
                stock=request.stock
            )

            return stock_by_store_pb2.StockByStoreResponse(
                store_id=stock_by_store.store_id,
                product_id=stock_by_store.product_id,
                stock=stock_by_store.stock
            )

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid argument: {str(e)}")
            return stock_by_store_pb2.StockByStoreResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {str(e)}")
            return stock_by_store_pb2.StockByStoreResponse()

    def SearchStockByStore(self, request, context) -> stock_by_store_pb2.StockByStoreListResponse:
        store_id = request.store_id if request.store_id else None
        product_id = request.product_id if request.product_id else None

        # Validar que al menos un parámetro de búsqueda haya sido proporcionado
        if all(param is None for param in [store_id, product_id]):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          "At least one search parameter must be provided.")

        # Llamar al repositorio para buscar el stock
        found_stocks = self.stock_by_store_repository.search_stoc
