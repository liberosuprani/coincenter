"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Número de aluno: 62220
"""
import sock_utils

class NetClient:
    def __init__(self, id, host, port):
        self._id = id
        self._host = host
        self._port = port
        self._socket = sock_utils.create_tcp_client_socket(host, port)
        self.send(f"{self._id}".encode())
     
    def send(self, data):
        self._socket.sendall(data)

    def recv(self):
        data = self._socket.recv(1024)
        return data
    
    def close(self):
        self._socket.close()