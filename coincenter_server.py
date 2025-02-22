"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""

import sys
import signal
from net_server import *
from coincenter_data import *

### código do programa principal ###
server = None

def handle_shutdown(signum, frame):
    global server
    server.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)
    
    global server

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    server = NetServer(server_ip, server_port)

    signal.signal(signal.SIGINT, handle_shutdown)

    ### código ###

if __name__ == "__main__":
    main()
