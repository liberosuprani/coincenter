"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""

import sys
from net_client import *
from coincenter_data import MANAGER_SUPPORTED_COMMANDS, USER_SUPPORTED_COMMANDS

USER_ID = 0
client = None

def manager_command_to_request(command):
    request = command
    args = []
    if command == "ADD_ASSET":
        args.append(input("Asset name > "))     # asset's name
        args.append(input("Asset symbol > "))    # asset's symbol 
        args.append(float(input("Asset price > ")))   # asset's price (cast to float)
        args.append(float(input("Available amount > ")))    # asset's available amount
    if command == "REMOVE_ASSET":
        args.append(input("Asset symbol > ")) # asset's symbol
    for arg in args:
        request += f";{arg}"
    request += ";0"     # manager id
    return request


def user_command_to_request(command):
    global USER_ID
    request = command
    args = []
    if command == "BUY" or command == "SELL":
        args.append(input("Asset symbol > "))   # asset's symbol 
        args.append(float(input("Quantity > ")))    # quantity to buy / sell
    if command == "DEPOSIT" or command == "WITHDRAW":
        args.append(float(input("Amount")))    # amount to deposit / withdraw
    for arg in args:
        request += f";{arg}"
    request += f";{USER_ID}"
    return request


def show_manager_menu():
    
    global client
    
    while True: 
        print("1) Add asset\n2) List all assets\n3) Remove an asset\n0) Exit")
        command_number = int(input("command > "))
        
        while command_number not in MANAGER_SUPPORTED_COMMANDS.keys():
            print("Command does not exist. Try again.")
            command_number = int(input("command > "))
            
        # gets the proper command from the dictionary with supported commands 
        command = MANAGER_SUPPORTED_COMMANDS[command_number]
        
        if command == "EXIT":
            client.close()
            return
        
        request = manager_command_to_request(command)
        
        print(f"SENT: {request}")
        request = request.encode()
        client.send(request)
        
        response = client.recv().decode()
        print(f"RECV: {response}")
  
            
def show_user_menu():
    
    global USER_ID, client
    
    while True:
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
        
        request = user_command_to_request(command)
        
        client.send(request.encode())
    # TODO implementar o recebimento da resposta do servidor


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