from sqlalchemy.orm import Session
from server.entities.store import Store


class StoreRepository:
    def __init__(self, session: Session):
        self.session = session

    def _validate_code(self, code: str) -> None:
        """Validates that the code is alphanumeric and meets length requirements."""
        if not code.isalnum():
            raise ValueError("Store code must be alphanumeric.")
        if len(code) < 3 or len(code) > 50:
            raise ValueError(
                "Store code must be between 3 and 50 characters long.")

    def create_store(self, code: str, address: str, city: str, state: str, enabled: bool) -> Store:
        
        code = code.upper()
        
        # Validar que el código sea alfanumérico
        self._validate_code(code)

        # Validar que otros campos no estén vacíos
        if not address or not city or not state:
            raise ValueError(
                "Address, city, and state fields cannot be empty.")

        # Crear una nueva instancia de Store
        store = Store(
            code=code,
            address=address,
            city=city,
            state=state,
            enabled=enabled
        )

        # Añadir la tienda a la sesión de la base de datos
        self.session.add(store)

        try:
            # Confirmar los cambios en la base de datos
            self.session.commit()
            # Refrescar la instancia para que refleje los datos guardados
            self.session.refresh(store)
        except Exception as e:
            # Si ocurre un error, hacer rollback y relanzar la excepción
            self.session.rollback()
            raise RuntimeError(
                f"An error occurred while creating the store: {str(e)}")

        # Devolver la tienda creada
        return store
    def get_store_by_id(self, store_id: int) -> Store:
        """Obtiene una tienda por su ID."""
        store = self.session.query(Store).filter(Store.id == store_id).first()
        
        if not store:
            raise ValueError(f"Store not found for the given id: {store_id}")
        
        return store
    
    def get_store_by_code(self, code: str) -> Store:
        return self.session.query(Store).filter(Store.code == code).first()

    def disable_store(self, code: str, enabled: bool) -> Store:
        store = self.get_store_by_code(code)

        if store:
            store.enabled = enabled
            self.session.commit()

            return store
        else:
            raise ValueError("Store not found")


    def search_store(self, code: str = None, enabled: bool = None):
        try:
            # Crear una consulta base
            query = self.session.query(Store)

            # Aplicar filtros según los parámetros de búsqueda proporcionados
            if code:
                query = query.filter(Store.code == code)

            # Aplicar el filtro solo si `enabled` no es None (ya que False es un valor válido)
            if enabled is not None:
                query = query.filter(Store.enabled == enabled)

            # Ejecutar la consulta
            stores = query.all()

            # Si no se encuentran tiendas, puedes manejarlo de la siguiente manera
            if not stores:
                raise ValueError("No stores found matching the search criteria.")

            # Devolver las tiendas encontradas
            return stores

        except Exception as e:
            # Realiza un rollback en caso de error para limpiar la sesión
            self.session.rollback()
            print(f"Error during store search: {e}")
            raise  # Re-lanza la excepción para que el cliente gRPC reciba el error
        finally:
            # Asegúrate de cerrar la sesión para liberar los recursos
            self.session.close()




