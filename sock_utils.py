"""
Aplicações Distribuídas - Projeto 1 - sock_utils.py
Número de aluno: 62220
"""
import socket as s
import sys

def create_tcp_server_socket(address='localhost', port=9999, queue_size=1):
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.bind((address, port))
        sock.listen(queue_size)
        return sock
    except:
        print("An error occurred during the creation of server socket.")
        sys.exit(1)
        
def create_tcp_client_socket(address='localhost', port=9999):
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect((address, port))
        return sock
    except:
        print("An error occurred during the creation of the client socket.")
        sys.exit(1)