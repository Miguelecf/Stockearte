from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos MySQL
DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/store_system"
engine = create_engine(DATABASE_URL)

# Declarative base
Base = declarative_base()

# Session para hacer operaciones con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
