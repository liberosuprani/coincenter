"""
Aplicações Distribuídas - Projeto 2 - coincenter_client.py
Número de aluno: 62220
"""

# import sys
import coincenter_data as consts
import requests, sys, json

session = requests.Session()
HOST = "http://localhost:5000/"

def validate_manager_command(command_and_args: list) -> bool:
    """
    Validates a manager command and its args.
    """
    command = command_and_args[0]

    if command == consts.ADD_ASSET:
        if len(command_and_args) != 5:
            return False
        try:
            asset_price = float(command_and_args[3])
            asset_available_quantity = int(command_and_args[4])
            if asset_price <= 0 or asset_available_quantity <= 0:
                return False
        except:
            return False
        else:
            return True

    if command == consts.GET_ALL_ASSETS:
        return len(command_and_args) == 1
    if command == consts.GET_ASSET:
        return len(command_and_args) == 2 and isinstance(command_and_args[1], str)
    if command == consts.EXIT:
        return len(command_and_args) == 1
    
    return True


# def validate_user_command(command_and_args: list) -> bool:
#     """
#     Validates a user command and its args.
#     """
#     command = command_and_args[0]

#     if command == consts.USER_SUPPORTED_COMMANDS[consts.USER_GET_ALL_ASSETS] or command == consts.USER_SUPPORTED_COMMANDS[consts.USER_GET_ASSETS_BALANCE]:
#         return len(command_and_args) == 1
    
#     if command == consts.USER_SUPPORTED_COMMANDS[consts.USER_BUY] or command == consts.USER_SUPPORTED_COMMANDS[consts.USER_SELL]:
#         if len(command_and_args) != 3:
#             return False
#         try:
#             quantity = float(command_and_args[2])
#             if quantity <= 0:
#                 return False
#         except:
#             return False
#         else:
#             return True
        
#     if command == consts.USER_SUPPORTED_COMMANDS[consts.USER_DEPOSIT] or command == consts.USER_SUPPORTED_COMMANDS[consts.USER_WITHDRAW]:
#         if len(command_and_args) != 2:
#             return False
#         try:
#             amount = float(command_and_args[1])
#             if amount <= 0:
#                 return False
#         except:
#             return False
#         else:
#             return True
    
#     if command == consts.USER_SUPPORTED_COMMANDS[consts.USER_EXIT]:
#         return len(command_and_args) == 1


def show_manager_menu(client_id):
    """
    Shows the manager menu and collects the input.
    """
    exit_program = False
    while not exit_program: 
        print("\n===============")
        print(f"{consts.ADD_ASSET}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.ADD_ASSET]}\n"
            f"{consts.GET_ALL_ASSETS}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_ALL_ASSETS]}\n"
            f"{consts.GET_ASSET}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_ASSET]}\n"
            f"{consts.EXIT}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.EXIT]}")

        exit_loop = False
        while not exit_loop or command[0] not in consts.MANAGER_SUPPORTED_COMMANDS.keys():
            send_request = None
            command = []
            command.append(int(input("command > ")))

            if command[0] == consts.ADD_ASSET:
                command.append(input("Asset name > "))     # asset's name
                command.append(input("Asset symbol > "))    # asset's symbol 
                command.append(float(input("Asset price > ")))   # asset's price (cast to float)
                command.append(float(input("Available quantity > ")))    # asset's available amount
                send_request = manager_add_asset

            # if command[0] == consts.MGR_REMOVE_ASSET:
            #     command.append(input("Asset symbol > ")) # asset's symbol
            #     action = manager_remove_asset

            if command[0] == consts.GET_ALL_ASSETS:
                send_request = get_all_assets

            if command[0] == consts.GET_ASSET:
                command.append(input("Asset symbol > "))
                send_request = get_asset

            if command[0] == consts.EXIT:
                exit_program = True
                break

            if not validate_manager_command(command):
                print("Invalid arguments were provided. Try again.")
            else:
                exit_loop = True
                r = send_request(command)
                print(r.text)


def manager_add_asset(command: list):
    name = command[1]
    symbol = command[2]
    price = command[3]
    available_quantity = command[4]
    asset = {
        "symbol" : symbol,
        "name" : name,
        "price" : price,
        "available_quantity" : available_quantity
    }
    return session.post(f"{HOST}asset", json=asset)


def get_all_assets(command):
    return session.get(f"{HOST}/assetset")


def get_asset(command: list):
    symbol = command[1]
    return session.get(f"{HOST}/asset/{symbol}")

# def show_user_menu():
#     """
#     Shows the user menu and collects the input.
#     """
#     global USER_ID, stub
    
#     while True:
#         print("\n===============")
#         print(f"{consts.USER_GET_ALL_ASSETS}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_GET_ALL_ASSETS]}\n"
#             f"{consts.USER_GET_ASSETS_BALANCE}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_GET_ASSETS_BALANCE]}\n"
#             f"{consts.USER_BUY}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_BUY]}\n"
#             f"{consts.USER_SELL}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_SELL]}\n"
#             f"{consts.USER_DEPOSIT}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_DEPOSIT]}\n"
#             f"{consts.USER_WITHDRAW}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_WITHDRAW]}\n"
#             f"{consts.USER_EXIT}) {consts.USER_SUPPORTED_COMMANDS[consts.USER_EXIT]}")
        
#         user_command = int(input("command > "))
#         user_command_with_args = []

#         valid_command_numbers = consts.USER_SUPPORTED_COMMANDS.keys()

#         while user_command not in valid_command_numbers and (user_command not in valid_commands or not validate_user_command(user_command_with_args)): 
#             print("Command does not exist or has invalid arguments. Try again.")
#             user_command = input("command > ")
#             if user_command.isdigit():
#                 user_command = int(user_command)
#             else:
#                 user_command_with_args = user_command.split(";")
#                 user_command = user_command_with_args[0]
        
#         # if command was a number, call the function that will ask for the args,
#         # else it will append the user id and assign it to the request variable
#         if user_command in valid_command_numbers:
#             request = user_command_to_request(user_command)
#         else:
#             user_command_with_args[0] = [number for number in consts.USER_SUPPORTED_COMMANDS.keys() if consts.USER_SUPPORTED_COMMANDS[number] == user_command][0]
#             user_command_with_args.append(USER_ID)
#             request = user_command_with_args

#         response = stub.send_request(request)
#         if request[0] == consts.USER_EXIT and response[1] == True:
#             stub.disconnect()
#             return

# def main():
    
#     global stub, USER_ID
    
#     if len(sys.argv) != 4:
#         print("Usage: python3 coincenter_client.py user_id server_ip server_port")
#         sys.exit(1)
    
#     USER_ID = int(sys.argv[1])
#     HOST = sys.argv[2]   
#     PORT = int(sys.argv[3]) 
    
#     if USER_ID < 0:
#         print("User id must be 0 (manager) or above (normal user)!")
#         sys.exit(1)
    
#     stub = CoincenterStub()
#     stub.connect(USER_ID, HOST, PORT)

#     if USER_ID == 0:
#         show_manager_menu()
#     else:
#         show_user_menu()



def login_menu():
    client_id = int(input("----------\nBem-vindo ao coincenter.\nIndique seu id: "))
    response = session.post("http://localhost:5000/login", json = {"client_id":client_id})
    response_json = json.loads(response.text)

    while response.status_code != 200:
        print(response_json["title"])
        client_id = int(input("Bem-vindo ao coincenter.\nIndique seu id: "))
        response = session.post("http://localhost:5000/login", json = {"client_id":client_id})

    if client_id == 0:
        show_manager_menu(client_id)
    # else:
    #     show_user_menu(client_id)

def main():
    login_menu()

if __name__ == "__main__":
    main()

