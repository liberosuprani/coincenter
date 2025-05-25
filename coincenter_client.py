"""
Aplicações Distribuídas - Projeto 3 - coincenter_client.py
Número de aluno: 62220
"""

import coincenter_data as consts
import requests, json
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch

session = requests.Session()
HOST = "https://localhost:5000/"


def validate_manager_command(command: int, args: list) -> bool:
    """
    Validates a manager command and its args.
    """

    if command == consts.ADD_ASSET:
        if len(args) != 4:
            return False
        try:
            asset_price = float(args[2])
            asset_available_quantity = int(args[3])
            if asset_price <= 0 or asset_available_quantity <= 0:
                return False
        except:
            return False
        else:
            return True

    if command == consts.GET_ALL_ASSETS:
        return len(args) == 0
    if command == consts.GET_ASSET:
        return len(args) == 1 and isinstance(args[0], str)
    if command == consts.GET_ASSET_SET:
        return len(args) >= 1
    if command == consts.GET_TRANSACTIONS:
        return len(args) == 0
    if command == consts.EXIT:
        return len(args) == 0
    
    return False


def validate_user_command(command: int, args: list) -> bool:
    """
    Validates a user command and its args.
    """

    if command == consts.GET_ALL_ASSETS or command == consts.GET_ASSETS_BALANCE:
        return len(args) == 0
    
    if command == consts.GET_ASSET:
        return len(args) == 1 and isinstance(args[0], str)

    if command == consts.GET_ASSET_SET:
        return len(args) >= 1

    if command == consts.BUY or command == consts.SELL:
        if len(args) != 2:
            return False
        try:
            quantity = float(args[1])
            if quantity <= 0:
                return False
        except:
            return False
        else:
            return True
        
    if command == consts.DEPOSIT or command == consts.WITHDRAW:
        if len(args) != 1:
            return False
        try:
            amount = float(args[0])
            if amount <= 0:
                return False
        except:
            return False
        else:
            return True
    
    if command == consts.EXIT:
        return len(args) == 0
    
    return False


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
            f"{consts.GET_ASSET_SET}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_ASSET_SET]}\n"
            f"{consts.GET_TRANSACTIONS}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_TRANSACTIONS]}\n"
            f"{consts.EXIT}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.EXIT]}")

        exit_loop = False
        command = None
        while not exit_loop and command not in consts.MANAGER_SUPPORTED_COMMANDS.keys():
            send_request = None
            args = []
            try:
                command = int(input("command > "))
            except ValueError as e:
                print("Invalid command.")
                continue

            if command == consts.ADD_ASSET:
                args.append(input("Asset name > "))     # asset's name
                args.append(input("Asset symbol > ").upper())    # asset's symbol 
                try:
                    args.append(float(input("Asset price > ")))   # asset's price (cast to float)
                    args.append(float(input("Available quantity > ")))    # asset's available amount
                except ValueError as e:
                    print("Invalid price or quantity.")
                send_request = manager_add_asset

            if command == consts.GET_ALL_ASSETS:
                send_request = get_all_assets

            if command == consts.GET_ASSET:
                args.append(input("Asset symbol > ").upper())
                send_request = get_asset

            if command == consts.GET_ASSET_SET:
                args.extend(input("Symbols (separated by space): ").strip().split())
                args = list(map(lambda s : s.upper(), args))
                send_request = get_asset_set

            if command == consts.GET_TRANSACTIONS:
                send_request = manager_get_transactions

            if command == consts.EXIT:
                exit_program = True
                break

            if not validate_manager_command(command, args):
                print("Command does not exist or has invalid arguments. Try again.")
            else:
                exit_loop = True
                r = send_request(args)
                print("\n", r.text)


def user_menu(client_id):
    """
    Shows the user menu and collects the input.
    """
    exit_program = False
    while not exit_program:
        print("\n===============")
        print(f"{consts.GET_ALL_ASSETS}) {consts.USER_SUPPORTED_COMMANDS[consts.GET_ALL_ASSETS]}\n"
            f"{consts.GET_ASSET}) {consts.MANAGER_SUPPORTED_COMMANDS[consts.GET_ASSET]}\n"
            f"{consts.GET_ASSET_SET}) {consts.USER_SUPPORTED_COMMANDS[consts.GET_ASSET_SET]}\n"
            f"{consts.GET_ASSETS_BALANCE}) {consts.USER_SUPPORTED_COMMANDS[consts.GET_ASSETS_BALANCE]}\n"
            f"{consts.BUY}) {consts.USER_SUPPORTED_COMMANDS[consts.BUY]}\n"
            f"{consts.SELL}) {consts.USER_SUPPORTED_COMMANDS[consts.SELL]}\n"
            f"{consts.DEPOSIT}) {consts.USER_SUPPORTED_COMMANDS[consts.DEPOSIT]}\n"
            f"{consts.WITHDRAW}) {consts.USER_SUPPORTED_COMMANDS[consts.WITHDRAW]}\n"
            f"{consts.EXIT}) {consts.USER_SUPPORTED_COMMANDS[consts.EXIT]}")
        
        exit_loop = False
        command = None
        while not exit_loop and command not in consts.USER_SUPPORTED_COMMANDS.keys(): 
            send_request = None
            args = []
            try:
                command = int(input("command > "))
            except ValueError as e:
                print("Invalid command.")
                continue

            if command == consts.GET_ALL_ASSETS:
                send_request = get_all_assets

            if command == consts.GET_ASSET:
                args.append(input("Asset symbol > ").upper())
                send_request = get_asset

            if command == consts.GET_ASSET_SET:
                args = input("Symbols (separated by space): ").strip().split()
                args = list(map(lambda s : s.upper(), args))
                send_request = get_asset_set

            if command == consts.GET_ASSETS_BALANCE:
                send_request = get_user_assets

            if command == consts.BUY or command == consts.SELL:
                args.append(input("Asset symbol > ").upper())   # asset's symbol 
                try:
                    args.append(float(input("Quantity > ")))    # quantity to buy / sell
                except ValueError as e:
                    print("Invalid quantity.")
                    continue
                send_request = user_buy_asset if command == consts.BUY else user_sell_asset 
                
            if command == consts.DEPOSIT or command == consts.WITHDRAW:
                try:
                    args.append(float(input("Amount > ")))    # amount to deposit / withdraw
                except ValueError as e:
                    print("Invalid quantity.")
                    continue
                send_request = user_deposit if command == consts.DEPOSIT else user_withdraw 

            if command == consts.EXIT:
                exit_program = True
                break

            if not validate_user_command(command, args):
                print("Command does not exist or has invalid arguments. Try again.")
            else:
                exit_loop = True
                r = send_request(args)
                print("\n", r.text)


########################### SEND FUNCTIONS

def get_user_assets(args):
    return session.get(f"{HOST}/user")

def user_buy_asset(args):
    symbol = args[0]
    quantity = args[1]
    buy_request = {
        "symbol" : symbol,
        "quantity" : quantity
    }
    return session.post(f"{HOST}/buy", json=buy_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def user_sell_asset(args):
    symbol = args[0]
    quantity = args[1]
    sell_request = {
        "symbol" : symbol,
        "quantity" : quantity
    }
    return session.post(f"{HOST}/sell", json=sell_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def user_deposit(args):
    amount = args[0]
    deposit_request = {
        "amount" : amount
    }
    return session.post(f"{HOST}/deposit", json=deposit_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def user_withdraw(args):
    amount = args[0]
    withdraw_request = {
        "amount" : amount
    }
    return session.post(f"{HOST}/withdraw", json=withdraw_request, verify="root.pem", cert=("cli.crt", "cli.key"))

def manager_add_asset(args: list):
    name = args[0]
    symbol = args[1]
    price = args[2]
    available_quantity = args[3]
    asset = {
        "symbol" : symbol,
        "name" : name,
        "price" : price,
        "available_quantity" : available_quantity
    }
    return session.post(f"{HOST}asset", json=asset, verify="root.pem", cert=("cli.crt", "cli.key"))

def manager_get_transactions(args):
    return session.get(f"{HOST}/transactions", verify="root.pem", cert=("cli.crt", "cli.key"))

def get_all_assets(args):
    return session.get(f"{HOST}/assetset", verify="root.pem", cert=("cli.crt", "cli.key"))

def get_asset_set(args):
    asset_set_request = ""

    for symbol in args:
        asset_set_request += f"{symbol} "

    return session.get(f"{HOST}/assetset/{asset_set_request}", verify="root.pem", cert=("cli.crt", "cli.key"))

def get_asset(args: list):
    symbol = args[0]
    return session.get(f"{HOST}/asset/{symbol}", verify="root.pem", cert=("cli.crt", "cli.key"))

###########################

first_watch = True
    
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
        zk = KazooClient(hosts="127.0.0.1:2181")
        zk.start()
        @ChildrenWatch(zk, "/asset")
        def watch_assets(assets):
            global first_watch
            if len(assets) > 0 and not first_watch:

                # the first split gets the symbol along with the sequence number
                # the second split gets the sequence number
                assets = sorted(assets, key=lambda a : int(a.split("/")[-1].split("-")[1]))
                new_asset = assets[-1]

                # the first split gets the symbol along with the sequence number
                # the second split gets the symbol
                asset_symbol = new_asset.split("/")[-1].split("-")[0]
                print(f"\n\n(ALERT)\nNew asset was added: {asset_symbol}\n")
            elif first_watch:
                first_watch = False

        user_menu(client_id)

def main():
    login_menu()

if __name__ == "__main__":
    main()

