"""
Aplicações Distribuídas - Projeto 1 - sock_utils.py
Número de aluno: 62220
"""

import socket as s
import sys, struct, pickle

def create_tcp_server_socket(address='localhost', port=9999, queue_size=1):
    """
    Creates a tcp socket for a server.
    
    Requires:
    - address str
    - port int
    - queue_size int (default=1) 
    
    Ensures:
    The socket created
    """
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.bind((address, port))
        sock.listen(queue_size)
        return sock
    except:
        print("An error occurred during the creation of server socket.")
        sys.exit(1)
        
def create_tcp_client_socket(address='localhost', port=9999):
    """
    Creates a socket for a client and connects it to a server.
    
    Requires:
    - address str
    - port int
    
    Ensures:
    The socket created
    """
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect((address, port))
        return sock
    except:
        print("An error occurred during the creation of the client socket.")
        sys.exit(1)

def receive_all(socket_receiver: s.socket):
    """
    Calls socket.recv twice for the given socket.
    The first call is to receive the size of the data, whereas the second
    is to receive the data itself.
    """
    try:
        data_size_bytes = socket_receiver.recv(4)
        data_size = struct.unpack("i", data_size_bytes)[0]
        data_bytes = socket_receiver.recv(data_size)
        data = pickle.loads(data_bytes)
    except:
        if data_size_bytes.decode() == "":
            raise s.error()
        else:
            print("An error occurred while receiving.")

    return data
