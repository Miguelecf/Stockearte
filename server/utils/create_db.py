from sqlalchemy.exc import SQLAlchemyError
from server.entities.base  import Base, SessionLocal, engine
from server.entities import product_store, user,store,product

def init_db():
    try:
        session = SessionLocal()
        Base.metadata.create_all(bind=engine)
        session.commit()
        print("Tablas creadas exitosamente.")
    except SQLAlchemyError as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()