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

# Enviar mensaje al tópico
for i in range(10):
    message = {'number': i}
    producer.send('test-topic', message)
    print(f"Mensaje enviado: {message}")
    time.sleep(1)

producer.flush()
producer.close()


