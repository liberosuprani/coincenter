"""
Aplicações Distribuídas - Projeto 2 - coincenter_stub.py
Número de aluno: 62220
"""

import socket
from net_client import *

class CoincenterStub:
    def __init__(self):
        self.conn_sock = None
        
    def connect(self, USER_ID, HOST, PORT):
        self.conn_sock = NetClient(USER_ID, HOST, PORT) 

    def disconnect(self):
        self.conn_sock.close()

    def send_request(self, request):
        try:
            self.conn_sock.send(request)
            print(f"\nSENT: {request}")
            
            response = self.conn_sock.receive_all()
            print(f"RECV: {response}")

            return response
        except socket.error as e:
            print(f"There was an error sending the request/receiving a response to/from the server. {e}")


