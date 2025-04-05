"""
Aplicações Distribuídas - Projeto 1 - net_server.py
Número de aluno: 62220
"""
import sock_utils
import socket as s
import pickle
import struct

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

    def send(self, response, client_socket):
        bytes_response = pickle.dumps(response)
        bytes_response_size = struct.pack("i", len(bytes_response))

        client_socket.sendall(bytes_response_size)
        client_socket.sendall(bytes_response)
        
    def close(self):
        self._socket.close()