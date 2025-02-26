"""
Aplicações Distribuídas - Projeto 1 - net_server.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""
import sock_utils

class NetServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket = sock_utils.create_tcp_server_socket(host, port)
    
    def accept(self):
        return self._socket.accept() 

    def recv(self, client_socket):
        data = client_socket.recv(1024)
        return data
    
    def send(self, data, client_socket):
        client_socket.sendall(data)
        
    def close(self):
        self._socket.close()