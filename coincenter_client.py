"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""

import sys
from net_client import *
from coincenter_data import ClientController, MANAGER_SUPPORTED_COMMANDS, USER_SUPPORTED_COMMANDS

USER_ID = 0
client = None

def show_manager_menu():
    
    global client
    
    print("1) Add asset\n2) List all assets\n3) Remove an asset\n0) Exit")
    command_number = int(input("command > "))
    
    print(f"teste: {MANAGER_SUPPORTED_COMMANDS.keys()}")
    while command_number not in MANAGER_SUPPORTED_COMMANDS.keys():
        print("Command does not exist. Try again.")
        command_number = int(input("command > "))
        
    # gets the proper command from the dictionary with supported commands 
    command = MANAGER_SUPPORTED_COMMANDS[command_number]
    
    if command == "EXIT":
        client.close()
        return
    
    # concatenates the command with this user's id
    request = command + ";0"
    client.send(request.encode())
            
def show_user_menu():
    
    global USER_ID, client
    
    print("1) List my assets\n2) See my balance\n3) Buy an asset\n4) Sell an asset\n5) Deposit\n6) Withdraw\n0) Exit")
    command_number = int(input("command > "))
    
    while command_number not in USER_SUPPORTED_COMMANDS.keys():
        print("Command does not exist. Try again.")
        command_number = int(input("command > "))
        
    # gets the proper command from the dictionary with supported commands 
    command = USER_SUPPORTED_COMMANDS[command_number]
    
    if command == "EXIT":
        client.close()
        return
    
    # concatenates the command with this user's id
    request = command + f"{USER_ID}"
    client.send(request.encode())

def main():
    
    global client, USER_ID
    
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)
    
    USER_ID = int(sys.argv[1])
    HOST = sys.argv[2]   
    PORT = int(sys.argv[3]) 
    
    if USER_ID < 0:
        print("User id must be 0 (manager) or above (normal user)!")
        sys.exit(1)
    
    client = NetClient(USER_ID, HOST, PORT) 
    
    if USER_ID == 0:
        show_manager_menu()
    else:
        show_user_menu()
    
if __name__ == "__main__":
    main()