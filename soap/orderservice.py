from spyne import Application, rpc, ServiceBase, Integer, Unicode, DateTime, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from datetime import datetime

class OrderService(ServiceBase):
    @rpc(Unicode, DateTime, DateTime, Integer, _returns=Iterable(Unicode))
    def get_orders(ctx, product_code, start_date, end_date, status):
        # Aquí iría la lógica para consultar las órdenes en la base de datos
        # Filtros: código de producto, rango de fechas y estado
        
        query = session.query(Order).filter(Order.request_date.between(start_date, end_date))
        if product_code:
            query = query.filter(Order.product_code == product_code)
        if status is not None:
            query = query.filter(Order.status == status)
        orders = query.all()
        for order in orders:
            yield f"Order {order.id}: {order.status.name}"
        orders = [
            f"Order 1: {product_code} - {status}",
            f"Order 2: {product_code} - {status}"
        ]
        for order in orders:
            yield order

application = Application([OrderService], 'urn:order_service',
                        in_protocol=Soap11(validator='lxml'),
                        out_protocol=Soap11())

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print("SOAP server listening on port 8000")
    server.serve_forever()
