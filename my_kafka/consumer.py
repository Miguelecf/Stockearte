from kafka import KafkaConsumer
import json 

# Configuración del consumidor
consumer = KafkaConsumer('test-topic',
                         bootstrap_servers = 'localhost:9092',
                         auto_offset_reset = 'earliest', #lastest = trae el mas reciente
                         enable_auto_commit = True,
                         group_id = 'test-group',
                         value_deserializer = lambda x: json.loads(x.decode('utf-8'))
                         )

print ("Esperando mensajes...")
for message in consumer:
    print(f"Mensaje recibido: {message.value}")