from kafka import KafkaConsumer
import json

# Configuración del consumidor
consumer = KafkaConsumer(
    'novedades',  
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Comienza desde el principio del log
    enable_auto_commit=True,
    group_id='novedades-group',  # Grupo de consumidores
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Esperando mensajes del tópico 'novedades'...")

for message in consumer:
    novedad_data = message.value
    product_code = novedad_data.get("product_code")
    sizes = novedad_data.get("sizes", [])
    photo_urls = novedad_data.get("photo_urls", [])

    # Procesar la información de la novedad
    print(f"\nNueva novedad recibida:")
    print(f"Código de producto: {product_code}")
    print(f"Talles disponibles con colores:")

    # Iterar sobre los tamaños y colores
    for size in sizes:
        size_label = size.get("size")
        colors = size.get("colors", [])

        # Asegurarse de que 'colors' es una lista de cadenas
        if isinstance(colors, list) and all(isinstance(c, str) for c in colors):
            print(f"- Talle: {size_label}, Colores: {', '.join(colors)}")
        else:
            print(f"- Talle: {size_label}, Colores: (formato incorrecto)")

    print("URLs de fotos:")
    for url in photo_urls:
        print(f"- {url}")
