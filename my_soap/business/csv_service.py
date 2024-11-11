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
DATABASE_URL = "mysql+pymysql://root:root@localhost/store_system"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CSVService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def upload_csv(ctx, csv_content):
        session = SessionLocal()
        data = []
        csv_content = csv_content.lstrip('\ufeff')
        csv_reader = csv.DictReader(StringIO(csv_content), delimiter=';')
        
        seen_usernames = set()
        errors = []
        
        for line_num, row in enumerate(csv_reader, start=1):
            print(f"Claves del diccionario: {list(row.keys())}")
            print("Fila leída:", row)

            if len(row) == 5:
                username = row["usuario"]
                
                # Verificación de campos vacíos
                if any(not value.strip() for value in row.values()):
                    errors.append(f"\nLínea {line_num}: Campos vacíos detectados.\n")
                    continue
                
                # Duplicidad en el CSV
                if username in seen_usernames:
                    errors.append(f"\nLínea {line_num}: Usuario duplicado en el CSV - '{username}'.\n")
                    continue
                
                seen_usernames.add(username)
                
                user_data = {
                    "usuario": username,
                    "contraseña": row["contraseña"],
                    "nombre": row["nombre"],
                    "apellido": row["apellido"],
                    "codigo de tienda": row["codigo de tienda"]
                }
                data.append(user_data)
            else:
                errors.append(f"\nLínea {line_num}: Número incorrecto de campos en la fila.\n")
        
        try:
            for row in data:
                store_code = row["codigo de tienda"]
                store = session.query(Store).filter(Store.code == store_code).first()

                if not store:
                    errors.append(f"\nLínea {line_num}: Tienda con código '{store_code}' no encontrada.\n")
                    continue
                
                if not store.enabled:
                    errors.append(f"\nLínea {line_num}: La tienda con código '{store_code}' está deshabilitada.\n")
                    continue

                user = User(
                    username=row["usuario"],
                    password=row["contraseña"],
                    first_name=row["nombre"],
                    last_name=row["apellido"],
                    store_id=store.id,
                    enabled=True
                )
                session.add(user)

            session.commit()
            
            # Formatear el mensaje final
            success_message = f"\nUsuarios procesados exitosamente: {len(data) - len(errors)}.\n"
            error_message = f"Errores encontrados:\n {len(errors)}"
            formatted_errors = "\n".join(f"\n - {error}" for error in errors)
            
            return f"{success_message}\n{error_message}\n{formatted_errors}"
        
        except Exception as e:
            session.rollback()
            print(f"Error al insertar los usuarios: {str(e)}")
            return f"Error al insertar los usuarios: {str(e)}"
        
        finally:
            session.close()

