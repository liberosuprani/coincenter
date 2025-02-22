"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""

import sys
from net_client import *

MANAGER_SUPPORTED_COMMANDS = [
    "ADD_ASSET",
    "GET_ALL_ASSETS",
    "REMOVE_ASSET",
    "EXIT",
]

USER_SUPPORTED_COMMANDS = [
    "GET_ALL_ASSETS",
    "GET_BALANCE",
    "BUY",
    "SELL",
    "DEPOSIT",
    "WITHDRAW",
    "EXIT"
]

### código do programa principal ###
def show_manager_menu():
    command = input("command > ")
    
    while command not in MANAGER_SUPPORTED_COMMANDS:
        print("Command does not exist. Try again.")
        command = input("command > ")
        
            
def show_user_menu():
    command = input("command > ")
    
    while command not in USER_SUPPORTED_COMMANDS:
        print("Command does not exist. Try again.")
        command = input("command > ")


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)
    USER_ID = sys.argv[1]
    
    # 
    if USER_ID < 0:
        print("User id must be 0 (manager) or above (normal user)!")
        sys.exit(1)
        
    if USER_ID == 0:
        show_manager_menu()
    else:
        show_user_menu()
    
if __name__ == "__main__":
    main()