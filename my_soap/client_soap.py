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
        # Hacer la solicitud al servicio SOAP
        try:
            # Cambié helloWorld() a say_hello(), que es la función definida en el servidor SOAP
            response = client.service.say_hello("World")
        except Exception as e:
            response = f"Error al conectar con el servicio: {e}"

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5051)  # Asegúrate de que esté en el puerto 5001
