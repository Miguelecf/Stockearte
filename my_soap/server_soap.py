# server_soap.py
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Definimos una aplicación Flask para el servidor
app = Flask(__name__)

# Definimos el servicio SOAP
class HelloWorldService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello, {name}!"

# Configuración de la aplicación SOAP
soap_app = Application(
    [HelloWorldService],
    tns='spyne.examples.hello',    # Espacio de nombres (namespace)
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
    app.run(debug=True)
