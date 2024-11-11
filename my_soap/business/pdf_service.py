import sys
import os

sys.path.append(os.path.abspath("C:/Users/Ariel Colaluci/stockearte"))

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://root:root@localhost/store_system"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from server.entities.product import Product

class PDFService:
    @staticmethod
    def generate_pdf(title):
        # Conectarse a la base de datos
        session = SessionLocal()

        try:
            # Obtener todos los productos
            products = session.query(Product).all()

            # Crear un buffer en memoria para el PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Título del PDF
            p.setFont("Times-Roman", 18)
            p.drawString(100, height - 100, title)
            
            # Contenido principal
            p.setFont("Times-Roman", 12)
            text_object = p.beginText(100, height - 130)
            text_object.setTextOrigin(100, height - 130)
            
            # Agregar información de productos al PDF
            content = "Productos:\n\n"
            for product in products:
                content += (f"Nombre: {product.name}\n"
                            f"Código Único: {product.unique_code}\n"
                            f"Tamaño: {product.size}\n"
                            f"Color: {product.color}\n"
                            f"Estado: {'Habilitado' if product.enabled else 'Deshabilitado'}\n")
                
                # Agregar una imagen si tiene URL
                if product.image_url:
                    content += f"Imagen URL: {product.image_url}\n"
                
                content += "\n"  # Añadir un espacio entre productos
            
            text_object.textLines(content)
            p.drawText(text_object)
            
            # Finalizar el PDF
            p.showPage()
            p.save()

            buffer.seek(0)
            return buffer

        except Exception as e:
            print(f"Error al generar el PDF: {str(e)}")
            return None
        finally:
            session.close()
