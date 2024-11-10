# run.py
# run.py
import subprocess
import time

def run_server():
    """Ejecuta el servidor SOAP."""
    subprocess.Popen(["python", "server_soap.py"])

def run_client():
    """Ejecuta el cliente SOAP."""
    subprocess.Popen(["python", "client_soap.py"])

if __name__ == "__main__":
    print("Iniciando el servidor y cliente SOAP...")
    
    # Ejecutamos el servidor y el cliente en paralelo
    run_server()
    
    # Le damos un tiempo de espera al servidor para que inicie primero (ajusta si es necesario)
    time.sleep(2)
    
    run_client()

    print("Servidor y cliente SOAP están corriendo.")
