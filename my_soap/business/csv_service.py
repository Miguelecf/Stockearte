# csv_service.py
import csv
from io import StringIO
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from zeep import Client

# Inicializamos la aplicación flask
app = Flask(__name__)

# Definimos el servicio SOAP


class CSVService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def upload_csv(ctx, csv_content):
        # Creamos un objeto StringIO para leer el contenido del archivo CSV

        data = []
        csv_reader = csv.reader(StringIO(csv_content), delimiter=';')
        
        for row in csv_reader:
            print("Fila leída:", row) # Quiero ver que fila imprime
        
        for row in csv_reader:
            if len(row) == 5:
                data.append({
                    "usuario": row[0],
                    "contraseña": row[1],
                    "nombre": row[2],
                    "apellido": row[3],
                    "codigo de tienda": row[4]
                })
            else:
                return "Error en la carga del archivo CSV"

            return f"Usuarios procesados:{len(data)}"


# Configuración de la aplicación SOAP
soap_app = Application(
    [CSVService],
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
