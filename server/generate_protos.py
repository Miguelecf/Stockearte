import subprocess
import os

# Obtén la ruta absoluta del directorio del script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Configura las rutas absolutas
proto_path = os.path.join(base_dir, "..", "protos")  # Ruta a protos
output_dir = os.path.join(base_dir, "src", "generated")  # Ruta para los archivos generados

# Verifica que la ruta de los protos exista
if not os.path.exists(proto_path):
    raise FileNotFoundError(f"El directorio de protos no existe: {proto_path}")

# Verifica que la ruta de salida exista
os.makedirs(output_dir, exist_ok=True)

# Verifica si el archivo user.proto existe
proto_file_path = os.path.join(proto_path, "user.proto")
if not os.path.isfile(proto_file_path):
    raise FileNotFoundError(f"El archivo proto no existe: {proto_file_path}")

# Genera los archivos Python desde el archivo .proto
subprocess.run([
    "python", "-m", "grpc_tools.protoc",
    f"--proto_path={proto_path}",
    f"--python_out={output_dir}",
    f"--grpc_python_out={output_dir}",
    proto_file_path
], check=True)

# Renombra los módulos generados para que usen el formato deseado
generated_files = [
    os.path.join(output_dir, "user_pb2.py"),
    os.path.join(output_dir, "user_pb2_grpc.py")
]

for file_path in generated_files:
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        # Reemplaza 'login_pb2' con 'src.generated.login_pb2' en el contenido del archivo
        content = content.replace('import user_pb2 as user__pb2', 'from src.generated import user_pb2 as user__pb2')

        with open(file_path, 'w') as file:
            file.write(content)

print("Archivos Protobuf generados y ajustados exitosamente.")


