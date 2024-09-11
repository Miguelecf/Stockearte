import sys
import os
sys.path.append(os.path.abspath('src'))
from src.app.grpc_server import serve

if __name__ == '__main__':
    serve()
    
    