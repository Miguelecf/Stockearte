from flask import Flask, render_template, request
from zeep import Client

app = Flask(__name__)

# URL del servicio WSDL del servidor SOAP
wsdl_url = "http://127.0.0.1:5000/soap?wsdl"

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        client = Client(wsdl_url)

        # Verifica que se subió un archivo
        if 'csv_file' not in request.files:
            response = "No se subió ningún archivo CSV"
        else:
            csv_file = request.files['csv_file']
            csv_content = csv_file.read().decode('utf-8')  # Lee el contenido como texto

            # Llamada al servicio SOAP para enviar el contenido del CSV
            try:
                response = client.service.upload_csv(csv_content)
            except Exception as e:
                response = f"Error al conectar con el servicio: {e}"

    return render_template("csv_mass_import.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5051)  # Ejecuta el cliente en el puerto 5051
