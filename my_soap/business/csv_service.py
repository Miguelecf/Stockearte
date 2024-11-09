import csv
from io import StringIO
from spyne import ServiceBase, rpc, Unicode
from server.entities.user import User
from server.entities.store import Store
from server.entities.product import Product
from server.entities.order import Order
from server.entities.order_item import OrderItem
from server.entities.product_store import ProductStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://root:1612@localhost/store_system"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class CSVService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def upload_csv(ctx, csv_content):
        # Crear la sesión dentro del contexto del servicio SOAP
        session = SessionLocal()

        data = []
        csv_content = csv_content.lstrip('\ufeff')

        csv_reader = csv.DictReader(StringIO(csv_content), delimiter=';')

        # Procesar las filas del CSV
        for row in csv_reader:
            print(f"Claves del diccionario: {list(row.keys())}")
            print("Fila leída:", row)

            if len(row) == 5:
                user_data = {
                    "usuario": row["usuario"],
                    "contraseña": row["contraseña"],
                    "nombre": row["nombre"],
                    "apellido": row["apellido"],
                    "codigo de tienda": row["codigo de tienda"]
                }
                data.append(user_data)
            else:
                return "Error en la carga del archivo CSV: Fila incorrecta"
        
        try:
            for row in data:
                print(f"Buscando tienda con código: {row['codigo de tienda']}")

                store = session.query(Store).filter(Store.code == row['codigo de tienda']).first()

                if store:
                    print(f"Tienda encontrada: {store.code} - {store.id}")
                    user = User(
                        username=row["usuario"],
                        password=row["contraseña"],
                        first_name=row["nombre"],
                        last_name=row["apellido"],
                        store_id=store.id
                    )
                    session.add(user)
                else:
                    print(f"Error: Tienda con código {row['codigo de tienda']} no encontrada.")
                    return f"Error: Tienda con código {row['codigo de tienda']} no encontrada."

            session.commit()
            return f"Usuarios procesados: {len(data)}"
        
        except Exception as e:
            session.rollback()
            print(f"Error al insertar los usuarios: {str(e)}")
            return f"Error al insertar los usuarios: {str(e)}"
        
        finally:
            session.close()
