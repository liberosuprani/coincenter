"""
Aplicações Distribuídas - Projeto 1 - net_server.py
Número de aluno: 62220
"""
import sock_utils
import socket as s

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
    
    def receive_all(self, client_socket):
        try:
            data = sock_utils.receive_all(client_socket)
        except s.error as e:
            raise s.error()


        return data

    # TODO mandar o tamanho da mensagem
    def send(self, data, client_socket):
        client_socket.sendall(data)
        
    def close(self):
        self._socket.close()