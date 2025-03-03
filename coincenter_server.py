"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Número de aluno: 62220
"""

import sys
import signal
from net_server import *
from coincenter_data import *

server = None

def handle_shutdown(signum, frame):
    global server
    server.close()
    sys.exit(0)

def main():
    
    global server
    signal.signal(signal.SIGINT, handle_shutdown)
    
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    server = NetServer(server_ip, server_port)
    (connection_socket, (addr, port)) = server.accept()
    
    id_received = server.recv(connection_socket).decode()
    print(f"Client connected: [Id: {id_received}, Address: {addr}, Port: {port}]")
    
    while True:
        request = server.recv(connection_socket)
        request = request.decode()
        
        # if the request is an empty string, it means the client has closed the connection
        # then, it will wait for another connection
        if request == "":   
            print("Client disconnected.")
            connection_socket.close()
            (connection_socket, (addr, port)) = server.accept()
            id_received = server.recv(connection_socket).decode()
            print(f"Client connected: [Id: {id_received}, Address: {addr}, Port: {port}]")
        else:
            print(f"RECV: {request}") 
            response = ClientController.process_request(request)
            
            server.send(response.encode(), connection_socket)
            print(f"SENT: {response}")

if __name__ == "__main__":
    main()
