from spyne import Application, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, send_file
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os
from business.pdf_service import PDFService  # Importamos PDFService desde pdf_service.py

# Directorio donde se guardará el PDF
output_dir = r'C:/Users/Ariel Colaluci/Stockearte/my_soap'

# Asegurarse de que el directorio exista
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Si no existe, crearlo

app = Flask(__name__)

# Configuración del servicio SOAP
class PDFSoapService(ServiceBase):
    @staticmethod
    def generate_pdf(ctx, title):
        # Llamamos al método de PDFService para generar el PDF
        pdf_buffer = PDFService.generate_pdf(title)

        # Verificamos si el PDF se generó correctamente
        if pdf_buffer:
            # Guardar el PDF en el sistema de archivos temporalmente
            file_path = os.path.join(output_dir, 'reporte_productos.pdf')
            with open(file_path, 'wb') as f:
                f.write(pdf_buffer.read())

            # Verificar si el archivo existe
            if os.path.exists(file_path):
                return file_path  # Retornar la ruta del archivo
            else:
                return "Error al generar el PDF"
        else:
            return "Error al generar el PDF"

# Configuración de la aplicación SOAP
soap_app = Application(
    [PDFSoapService],  # Usamos PDFSoapService
    tns='spyne.pdf.service',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

# Integrar la aplicación SOAP con Flask
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': WsgiApplication(soap_app)  # Asegúrate de que esté en la ruta '/soap'
})

# Ruta para descargar el PDF generado
@app.route('/export-pdf')
def download_pdf():
    try:
        # Llamamos al servicio SOAP para generar el PDF
        file_path = PDFSoapService.generate_pdf(None, "Reporte de Productos")  # Título de ejemplo

        # Verificar si el archivo existe
        if os.path.exists(file_path):
            # Retornar el archivo PDF para su descarga
            return send_file(file_path, as_attachment=True, download_name='reporte_productos.pdf', mimetype='application/pdf')
        else:
            return "Archivo no encontrado", 404
    except Exception as e:
        return f"Error al enviar el archivo: {str(e)}", 500

# Ejecutar el servidor SOAP
if __name__ == "__main__":
    print("Servidor SOAP corriendo en http://127.0.0.1:9098/soap?wsdl")
    app.run(port=9098)
