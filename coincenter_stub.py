import pickle, socket
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
            bytes_request = pickle.dumps(request)
            self.conn_sock.send(bytes_request)
            print(f"\nSENT: {request}")

            bytes_response = self.conn_sock.recv()

            response = pickle.loads(bytes_response)
            print(f"RECV: {response}")
            
            return response
        except socket.error as e:
            print(f"There was an error communicating with the server. {e}")