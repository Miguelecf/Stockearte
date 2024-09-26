from sqlalchemy.orm import Session, Query
from server.entities.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product(
        self,
        name: str,
        unique_code: str,
        size: str,
        image_url: str,
        color: str,
        enabled: bool,
    ) -> Product:

        # Valida que otros campos no estén vacíos
        #   if not name or not unique_code or not size or not image_url or not color:
        #      raise ValueError("Name, unique_code, size, image_url and color fields cannot be empty.")
        print("repository", name, unique_code, size, image_url, color, enabled)

        product = Product(
            name=name,
            unique_code=unique_code,
            size=size,
            image_url=image_url,
            color=color,
            enabled=enabled,
        )

        # Añadir el producto a la sesión de la base de datos
        self.session.add(product)

        try:
            # Confirmar los cambios en la base de datos
            self.session.commit()
            # Refrescar la instancia para que refleje los datos guardados
            self.session.refresh(product)
        except Exception as e:
            # Si ocurre un error, hacer rollback y relanzar la excepción
            self.session.rollback()
            raise RuntimeError(
                f"An error occurred while creating the product: {str(e)}"
            )

        # Devolver el producto creada
        return product

    def get_product_by_code(self, unique_code: str) -> Product:
        print("En el get_product", unique_code)
        try:
            product = (
                self.session.query(Product)
                .filter(Product.unique_code == unique_code)
                .first()
            )
            return product
        except Exception as e:
            # Manejo de errores, puede ser registro de logs o lanzar una excepción personalizada
            raise RuntimeError(
                f"Error retrieving product by unique code {
                    unique_code}: {str(e)}"
            )

    def update_product(
        self,
        unique_code: str,
        name: str = None,
        size: str = None,
        color: str = None,
        image_url: str = None,
        enabled: bool = None,
    ):

        print(f"Unique code passed to query: {unique_code}")

        if not unique_code:
            raise ValueError("Unique code is required to update a product.")

        product = self.session.query(Product).filter(Product.unique_code == unique_code).first()
        # product = self.get_product_by_code(unique_code)
        if not product:
            raise ValueError(f"Product with unique_code {unique_code} not found.")

        # Actualizar solo si se proporciona un nuevo valor y no es None ni vacío
        if name not in [None, ""]:
            product.name = name
        if size not in [None, ""]:
            product.size = size
        if color not in [None, ""]:
            product.color = color
        if image_url not in [None, ""]:
            product.image_url = image_url
        
        if enabled is not None:  # Esto permite True y False
            product.enabled = enabled

        try:
            self.session.commit()
            self.session.refresh(product)
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"An error occurred while updating the product with unique_code {unique_code}: {str(e)}")

        return product


    def search_product(
        self,
        name: str = None,
        unique_code: str = None,
        size: str = None,
        color: str = None,
    ):
        # Crear una consulta base
        query = self.session.query(Product)

        # Aplicar filtros según los parámetros de búsqueda proporcionados
        if unique_code:
            query = query.filter(Product.unique_code == unique_code)
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        if size:
            query = query.filter(Product.size.ilike(f"%{size}%"))
        if color:
            query = query.filter(Product.color.ilike(f"%{color}%"))

        # Ejecutar la consulta
        products = query.all()

        # Si no se encuentran productos, puedes manejarlo de la siguiente manera
        if not products:
            raise ValueError("No products found matching the search criteria.")

        # Devolver los productos encontrados
        return products

    def disable_product(self, unique_code: str, enabled: bool) -> Product:
        # Obtener el producto por su código único
        product = self.get_product_by_code(unique_code)
        
        if product:
            # Cambiar el estado de habilitación del producto
            product.enabled = enabled
            
            try:
                # Confirmar los cambios en la base de datos
                self.session.commit()
                return product
            except Exception as e:
                # Si ocurre un error, hacer rollback y relanzar la excepción
                self.session.rollback()
                raise RuntimeError(
                    f"An error occurred while disabling the product: {str(e)}"
                )
        else:
            raise ValueError("Product not found")
