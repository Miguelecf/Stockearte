import os
from grpc_tools import protoc

# Función para generar los archivos gRPC a partir de un archivo .proto
def generate_proto(proto_name):
    print(f"Generando archivos para {proto_name}...")

    # Define paths
    proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'proto'))  # Ruta al directorio proto
    proto_file = os.path.join(proto_dir, f'{proto_name}.proto')  # Ruta al archivo .proto
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated'))

    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Verifica si el archivo .proto existe
    if not os.path.exists(proto_file):
        print(f"Error: {proto_name}.proto no existe en {proto_dir}.")
        return
    
    # Llamar a grpc_tools.protoc directamente para generar los archivos *_pb2.py y *_pb2_grpc.py
    result = protoc.main((
        '',
        f'-I{proto_dir}',
        f'--python_out={output_dir}',
        f'--grpc_python_out={output_dir}',
        proto_file,
    ))

    # Verificar si la generación fue exitosa
    if result == 0:
        print(f"Archivos generados exitosamente para {proto_name}.proto en {output_dir}.")
    else:
        print(f"Error al generar archivos para {proto_name}.proto")

# Sección USER.PROTO
# Llamar a la función para generar el archivo correspondiente a user.proto
generate_proto('user')
generate_proto('store')
generate_proto('product')
generate_proto('product_store')