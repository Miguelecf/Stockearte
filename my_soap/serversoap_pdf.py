from spyne import Application, ServiceBase, Integer, String, Array, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import base64
from fpdf import FPDF  # Usamos FPDF para generar el PDF

# Definimos el servicio SOAP que generará el PDF
class PDFService(ServiceBase):
    
    # Método para generar el PDF
    @staticmethod
    def generate_pdf(ctx, title):
        try:
            # Generación del PDF con FPDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Reporte de Productos: {title}", ln=True, align='C')

            # Aquí puedes agregar más contenido al PDF (por ejemplo, productos desde la base de datos)
            pdf.ln(10)  # Salto de línea
            pdf.multi_cell(0, 10, txt="Aquí irían los productos y sus detalles...")

            # Guardamos el PDF en memoria y lo convertimos a Base64
            pdf_output = pdf.output(dest='S').encode('latin1')  # 'S' significa que lo guarda en memoria
            pdf_base64 = base64.b64encode(pdf_output).decode('utf-8')  # Convertimos el PDF a Base64

            return pdf_base64
        except Exception as e:
            return str(e)

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación SOAP
soap_app = Application(
    [PDFService],  # Usamos PDFService en lugar de CSVService
    tns='spyne.pdf.service',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

# Integrar la aplicación SOAP con Flask
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': WsgiApplication(soap_app)
})

# Ejecutar el servidor
if __name__ == "__main__":
    print("Servidor SOAP corriendo en http://127.0.0.1:9098/soap?wsdl")
    app.run(port=9098)
