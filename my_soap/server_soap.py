# server_soap.py
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from business.csv_service import CSVService  # Importamos el servicio desde csv_service.py

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación SOAP
soap_app = Application(
    [CSVService],  # Usamos CSVService desde csv_service.py
    tns='spyne.csv.service',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

# Integrar la aplicación SOAP con Flask
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap': WsgiApplication(soap_app)
})

# Ejecutar el servidor
if __name__ == "__main__":
    print("Servidor SOAP corriendo en http://127.0.0.1:5000/soap?wsdl")
    app.run(port=5000)
