"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Número de aluno: 62220
"""

import sys
from coincenter_stub import *
from coincenter_data import MANAGER_SUPPORTED_COMMANDS, USER_SUPPORTED_COMMANDS

USER_ID = 0
stub = None

def manager_command_to_request(command_number) -> str:
    """
    Parses a manager command into a request for the server.
    
    Requires:
    - command str
    
    Ensures:
    A concatenation of the given command with the arguments needed for it.
    """
    request = [command_number]
    
    if command_number == MANAGER_SUPPORTED_COMMANDS[1]:
        request.append(input("Asset name > "))     # asset's name
        request.append(input("Asset symbol > "))    # asset's symbol 
        request.append(float(input("Asset price > ")))   # asset's price (cast to float)
        request.append(float(input("Available amount > ")))    # asset's available amount
    
    if command_number == MANAGER_SUPPORTED_COMMANDS[3]:
        request.append(input("Asset symbol > ")) # asset's symbol
    
    request.append(0)     # manager's id
    return request


def user_command_to_request(command_number) -> str:
    """
    Parses a user command into a request for the server.
    
    Requires:
    - command str
    
    Ensures:
    A concatenation of the given command with the arguments needed for it.
    """
    global USER_ID
    request = [command_number]
    
    if command_number == USER_SUPPORTED_COMMANDS[3] or command_number == USER_SUPPORTED_COMMANDS[4]:
        request.append(input("Asset symbol > "))   # asset's symbol 
        request.append(float(input("Quantity > ")))    # quantity to buy / sell
    
    if command_number == USER_SUPPORTED_COMMANDS[5] or command_number == USER_SUPPORTED_COMMANDS[6]:
        request.append(float(input("Amount > ")))    # amount to deposit / withdraw
    
    request.append(USER_ID)
    return request


def show_manager_menu():
    """
    Shows the manager menu and collects the input.
    """
    global stub
    
    while True: 
        print("\n===============")
        print("10) Add asset\n20) List all assets\n30) Remove an asset\n40) Exit")
        command_number = int(input("command > "))
        
        while command_number not in MANAGER_SUPPORTED_COMMANDS.keys():
            print("ERROR: Command does not exist. Try again.")
            command_number = int(input("command > "))
            
        # gets the proper command from the dictionary with supported commands 
        command = MANAGER_SUPPORTED_COMMANDS[command_number]
        
        if command == "EXIT":
            stub.close()
            return
        
        request = manager_command_to_request(command_number)

        stub.process_request(request)


def show_user_menu():
    """
    Shows the user menu and collects the input.
    """
    global USER_ID, stub
    
    while True:
        print("\n===============")
        print("50) List all assets\n60) See my balance\n70) Buy an asset\n80) Sell an asset\n90) Deposit\n100) Withdraw\n110) Exit")
        command_number = int(input("command > "))
        
        while command_number not in USER_SUPPORTED_COMMANDS.keys():
            print("Command does not exist. Try again.")
            command_number = int(input("command > "))
            
        # gets the proper command from the dictionary with supported commands 
        command = USER_SUPPORTED_COMMANDS[command_number]
        
        if command == "EXIT":
            stub.close()
            return
        
        request = user_command_to_request(command)
        
        stub.process_request(request)


def main():
    
    global stub, USER_ID
    
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)
    
    USER_ID = int(sys.argv[1])
    HOST = sys.argv[2]   
    PORT = int(sys.argv[3]) 
    
    if USER_ID < 0:
        print("User id must be 0 (manager) or above (normal user)!")
        sys.exit(1)
    
    stub = CoincenterStub()
    stub.connect(USER_ID, HOST, PORT)

    if USER_ID == 0:
        show_manager_menu()
    else:
        show_user_menu()
    
if __name__ == "__main__":
    main()