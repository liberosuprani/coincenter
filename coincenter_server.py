"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Número de aluno: 62220
"""

import sys, signal, select
from net_server import *
from coincenter_skeleton import *


def handle_shutdown(signum, frame):
    global server
    server.close()
    sys.exit(0)

server = None
socket_list = []

def main():
    
    global server, socket_list

    signal.signal(signal.SIGINT, handle_shutdown)
    
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    server = NetServer(server_ip, server_port)
    socket_list = [server._socket]

    skeleton = CoincenterSkeleton()

    while True:
        R, W, X = select.select(socket_list, [], [])
        for s in R:
            if s is server._socket:
                (connection_socket, (addr, port)) = server.accept()
                id_received = server.recv(connection_socket).decode()
                socket_list.append(connection_socket)
                print(f"Client connected: [Id: {id_received}, Address: {addr}, Port: {port}]")
            else:
                try:
                    request = server.receive_all(s)
                    print(f"RECV: {request}") 

                    response = skeleton.process_request(request)
                    server.send(response, s)
                except:
                    s.close()
                    socket_list.remove(s)
                    print("Client disconnected.")
                
            
if __name__ == "__main__":
    main()
