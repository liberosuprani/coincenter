"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Número de aluno: 62220
"""

import pickle
import socket as s

import sock_utils, struct

class NetClient:
    def __init__(self, id, host, port):
        self._id = id
        self._host = host
        self._port = port
        self._socket = sock_utils.create_tcp_client_socket(host, port)
        
        # sends the client's id to the server
        self.send_my_info(f"{self._id}")
     
    def send_my_info(self, info):
        """
        Sends the given info to the server
        """
        info = info.encode()
        self._socket.sendall(info)

    def send(self, request):
        bytes_request = pickle.dumps(request)
        bytes_request_size = struct.pack("i", len(bytes_request))
        self._socket.sendall(bytes_request_size)
        self._socket.sendall(bytes_request)
        
    def recv(self):
        data = self._socket.recv(1024)
        return data
    
    def receive_all(self):
        try:
            data = sock_utils.receive_all(self._socket)
        except s.error as e:
            raise s.error()
        return data
    
    def close(self):
        self._socket.close()