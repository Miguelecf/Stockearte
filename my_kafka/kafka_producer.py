from kafka import KafkaProducer
import json
import time


# Tiene que estar andando tanto el kafka como el zookeeper
'''
Windows:
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
.\bin\windows\kafka-server-start.bat .\config\server.properties

MacOs:
brew services start zookeeper
brew services start kafka
'''

# Configuración del productor
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(
                            v).encode('utf-8')
                         )

def send_order_to_kafka(store_code, observations, order_id, items, request_date):
    message = {
        "store_code": store_code,
        "observations": observations,  # Observaciones aquí
        "order_id": order_id,
        "items": items,
        "request_date": request_date
    }
    producer.send('orden-de-compra', message)
    producer.flush()
    print(f"Mensaje enviado a Kafka: {message}")

def process_order(order, store_repository, request_date):
    try:
        # Obtén la tienda por su ID
        store = store_repository.get_store_by_id(order.store_id)

        if not store:
            raise ValueError("Store not found.")

        # Obtén el código de la tienda
        store_code = store.code  # Aquí obtienes el código como string

        # Extraer las observaciones desde el objeto order
        observations = order.observations  # Aquí se extraen las observaciones

        # Llama a la función de enviar el mensaje a Kafka
        send_order_to_kafka(
            store_code=store_code, 
            observations=observations,  # Envías las observaciones a Kafka
            order_id=order.id,
            items=[{
                "id": item.id,
                "order_id": item.order_id,
                "item_code": item.item_code,
                "color": item.color,
                "size": item.size,
                "quantity": item.quantity
            } for item in order.items],
            request_date=request_date.ToDatetime().strftime("%Y-%m-%d %H:%M:%S")  # Formato amigable para la fecha
        )

    except ValueError as e:
        print(f"Error: {str(e)}")

