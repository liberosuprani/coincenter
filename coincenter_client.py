"""
Aplicações Distribuídas - Projeto 2 - coincenter_client.py
Número de aluno: 62220
"""

# import sys
import coincenter_data as consts
import requests, json

session = requests.Session()
HOST = "https://localhost:5000/"

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


def validate_user_command(command_and_args: list) -> bool:
    """
    Validates a user command and its args.
    """
    command = command_and_args[0]

    if command == consts.GET_ALL_ASSETS or command == consts.GET_ASSETS_BALANCE:
        return len(command_and_args) == 1
    
    if command == consts.BUY or command == consts.SELL:
        if len(command_and_args) != 3:
            return False
        try:
            quantity = float(command_and_args[2])
            if quantity <= 0:
                return False
        except:
            return False
        else:
            return True
        
    if command == consts.DEPOSIT or command == consts.WITHDRAW:
        if len(command_and_args) != 2:
            return False
        try:
            amount = float(command_and_args[1])
            if amount <= 0:
                return False
        except:
            return False
        else:
            return True
    
    if command == consts.EXIT:
        return len(command_and_args) == 1


########################### MENU

def manager_menu(client_id):
    """
    Shows the manager menu and collects the input.
    """
    exit_program = False
    while not exit_program: 
        print("\n===============")
        print(f"{consts.ADD_ASSET}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.ADD_ASSET]}\n"
            f"{consts.GET_ALL_ASSETS}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_ALL_ASSETS]}\n"
            f"{consts.GET_ASSET}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_ASSET]}\n"
            f"{consts.GET_TRANSACTIONS}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_TRANSACTIONS]}\n"
            f"{consts.EXIT}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.EXIT]}")

        exit_loop = False
        command = [""]
        while not exit_loop and command[0] not in consts.MANAGER_SUPPORTED_COMMANDS.keys():
            send_request = None
            command = []
            command.append(int(input("command > ")))

            if command[0] == consts.ADD_ASSET:
                command.append(input("Asset name > "))     # asset's name
                command.append(input("Asset symbol > "))    # asset's symbol 
                command.append(float(input("Asset price > ")))   # asset's price (cast to float)
                command.append(float(input("Available quantity > ")))    # asset's available amount
                send_request = manager_add_asset

            if command[0] == consts.GET_ALL_ASSETS:
                send_request = get_all_assets

            if command[0] == consts.GET_ASSET:
                command.append(input("Asset symbol > "))
                send_request = get_asset

            if command[0] == consts.GET_TRANSACTIONS:
                send_request = manager_get_transactions

            if command[0] == consts.EXIT:
                exit_program = True
                break

            if not validate_manager_command(command):
                print("Command does not exist or has invalid arguments. Try again.")
            else:
                exit_loop = True
                r = send_request(command)
                print(r.text)


def user_menu(client_id):
    """
    Shows the user menu and collects the input.
    """
    exit_program = False
    while not exit_program:
        print("\n===============")
        print(f"{consts.GET_ALL_ASSETS}) {consts.USER_SUPPORTED_COMMANDS[consts.GET_ALL_ASSETS]}\n"
            f"{consts.GET_ASSETS_BALANCE}) {consts.USER_SUPPORTED_COMMANDS[consts.GET_ASSETS_BALANCE]}\n"
            f"{consts.BUY}) {consts.USER_SUPPORTED_COMMANDS[consts.BUY]}\n"
            f"{consts.SELL}) {consts.USER_SUPPORTED_COMMANDS[consts.SELL]}\n"
            f"{consts.DEPOSIT}) {consts.USER_SUPPORTED_COMMANDS[consts.DEPOSIT]}\n"
            f"{consts.WITHDRAW}) {consts.USER_SUPPORTED_COMMANDS[consts.WITHDRAW]}\n"
            f"{consts.EXIT}) {consts.USER_SUPPORTED_COMMANDS[consts.EXIT]}")
        
        exit_loop = False
        command = [""]
        while not exit_loop and command[0] not in consts.USER_SUPPORTED_COMMANDS.keys(): 
            send_request = None
            command = []
            command.append(int(input("command > ")))
            
            if command[0] == consts.GET_ALL_ASSETS:
                send_request = get_all_assets

            if command[0] == consts.GET_ASSETS_BALANCE:
                send_request = get_user_assets

            if command[0] == consts.BUY or command[0] == consts.SELL:
                command.append(input("Asset symbol > "))   # asset's symbol 
                command.append(float(input("Quantity > ")))    # quantity to buy / sell
                send_request = user_buy_asset if command[0] == consts.BUY else user_sell_asset 
                
            if command[0] == consts.DEPOSIT or command[0] == consts.WITHDRAW:
                command.append(float(input("Amount > ")))    # amount to deposit / withdraw
                send_request = user_deposit if command[0] == consts.DEPOSIT else user_withdraw 

            if command[0] == consts.EXIT:
                exit_program = True
                break

            if not validate_user_command(command):
                print("Command does not exist or has invalid arguments. Try again.")
            else:
                exit_loop = True
                r = send_request(command)
                print(r.text)


########################### SEND FUNCTIONS

def get_user_assets(command):
    return session.get(f"{HOST}/user")

def user_buy_asset(command):
    symbol = command[1]
    quantity = command[2]
    buy_request = {
        "symbol" : symbol,
        "quantity" : quantity
    }
    return session.post(f"{HOST}/buy", json=buy_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def user_sell_asset(command):
    symbol = command[1]
    quantity = command[2]
    sell_request = {
        "symbol" : symbol,
        "quantity" : quantity
    }
    return session.post(f"{HOST}/sell", json=sell_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def user_deposit(command):
    amount = command[1]
    deposit_request = {
        "amount" : amount
    }
    return session.post(f"{HOST}/deposit", json=deposit_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def user_withdraw(command):
    amount = command[1]
    withdraw_request = {
        "amount" : amount
    }
    return session.post(f"{HOST}/withdraw", json=withdraw_request, verify="root.pem", cert=("cli.crt", "cli.key"))

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
    return session.post(f"{HOST}asset", json=asset, verify="root.pem", cert=("cli.crt", "cli.key"))

def manager_get_transactions(command):
    return session.get(f"{HOST}/transactions", verify="root.pem", cert=("cli.crt", "cli.key"))

def get_all_assets(command):
    return session.get(f"{HOST}/assetset", verify="root.pem", cert=("cli.crt", "cli.key"))

def get_asset(command: list):
    symbol = command[1]
    return session.get(f"{HOST}/asset/{symbol}", verify="root.pem", cert=("cli.crt", "cli.key"))

###########################

def login_menu():
    client_id = int(input("----------\nBem-vindo ao coincenter.\nIndique seu id: "))
    response = session.post("https://localhost:5000/login", json = {"client_id":client_id}, verify="root.pem", cert=("cli.crt", "cli.key"))
    response_json = json.loads(response.text)

    while response.status_code != 200:
        print(response_json["title"])
        client_id = int(input("Bem-vindo ao coincenter.\nIndique seu id: "))
        response = session.post("https://localhost:5000/login", json = {"client_id":client_id}, verify="root.pem", cert=("cli.crt", "cli.key"))

    if client_id == 0:
        manager_menu(client_id)
    else:
        user_menu(client_id)

def main():
    login_menu()

if __name__ == "__main__":
    main()

