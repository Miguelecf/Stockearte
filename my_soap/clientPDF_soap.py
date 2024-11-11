from flask import Flask, render_template, request, jsonify
from zeep import Client
import base64

app = Flask(__name__)

# URL del servicio WSDL del servidor SOAP
wsdl_url = "http://127.0.0.1:9098/soap?wsdl"  # Cambia esta URL por la de tu servicio

@app.route("/soap/export-pdf", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        client = Client(wsdl_url)

        # Verifica que se haya enviado el título para el PDF
        title = request.form.get('title', '')
        if not title:
            response = "Se debe proporcionar un título para el PDF"
        else:
            try:
                # Llamada al servicio SOAP para generar el PDF
                pdf_base64 = client.service.generate_pdf(title)

                if pdf_base64:
                    # Decodifica el archivo PDF desde Base64
                    pdf_data = base64.b64decode(pdf_base64)

                    # Prepara el PDF para ser mostrado como un archivo adjunto en la respuesta
                    response = jsonify({"message": "PDF generado con éxito"})
                    response.headers['Content-Type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = 'inline; filename="reporte_productos.pdf"'
                    response.set_data(pdf_data)
                else:
                    response = "Error al generar el PDF"
            except Exception as e:
                response = f"Error al conectar con el servicio: {e}"

    return render_template("pdf_form.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, port=9099)  # Ejecuta el cliente en el puerto 9099
