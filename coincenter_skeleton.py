"""
Aplicações Distribuídas - Projeto 2 - coincenter_server.py
Número de aluno: 62220
"""

from coincenter_data import *
import coincenter_data as consts

def validate_manager_request(command_and_args: list) -> bool:
    """
    Validates a manager command and its args.
    """
    command = command_and_args[0]

    if command == consts.MGR_ADD_ASSET:
        if len(command_and_args) != 5:
            return False
        try:
            asset_price = float(command_and_args[3])
            asset_available_supply = int(command_and_args[4])
            if asset_price <= 0 or asset_available_supply <= 0:
                return False
        except:
            return False
        else:
            return True

    if command == consts.MGR_GET_ALL_ASSETS:
        return len(command_and_args) == 1
    if command == consts.MGR_REMOVE_ASSET:
        return len(command_and_args) == 2
    if command == consts.MGR_EXIT:
        return len(command_and_args) == 1


def validate_user_request(command_and_args: list) -> bool:
    """
    Validates a user command and its args.
    """
    command = command_and_args[0]

    if command == consts.USER_GET_ALL_ASSETS or command == consts.USER_GET_ASSETS_BALANCE:
        return len(command_and_args) == 1
    
    if command == consts.USER_BUY or command == consts.USER_SELL:
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
        
    if command == consts.USER_DEPOSIT or command == consts.USER_WITHDRAW:
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
    
    if command == consts.USER_EXIT:
        return len(command_and_args) == 1


class CoincenterSkeleton:
    def __init__(self):
        self.response = []

    def manager_add_asset(self, client: Manager, asset_name: str, asset_symbol: str, asset_price: float, asset_available_supply: int):
        self.response = client.add_asset(asset_name, asset_symbol, asset_price, asset_available_supply)
        
    def manager_get_all_assets(self, client: Manager):
        self.response = client.get_all_assets()

    def manager_remove_asset(self, client: Manager, asset_symbol):
        self.response = client.remove_asset(asset_symbol)

    def user_get_all_assets(self, client: User):
        self.response = client.get_all_assets()

    def user_get_assets_balance(self, client: User):
        self.response = client.get_assets_balance()

    def user_buy_asset(self, client: User, asset_symbol: str, quantity: float):
        self.response = client.buy_asset(asset_symbol, quantity)

    def user_sell_asset(self, client: User, asset_symbol: str, quantity: float):
        self.response = client.sell_asset(asset_symbol, quantity)

    def user_deposit(self, client: User, amount: float):
        self.response = client.deposit(amount)

    def user_withdraw(self, client: User, amount: float):
        self.response = client.withdraw(amount)

    def process_request(self, request) -> tuple[int, list]:
        try:
            request_command_number = request[0]
            request_id = int(request[-1])
            
            client = ClientController.get_client(request_id)

            if request_command_number == USER_EXIT or request_command_number == MGR_EXIT:
                self.response = [request_command_number+1, True]
                print(f"SENT: {self.response}") 
                return self.response

            elif request_id == 0:
                # validates manager request without the last argument (id)
                is_command_valid = validate_manager_request(request[:-1])

                if not is_command_valid:
                    self.response = [0, "Error: invalid command"]
                    print(f"SENT: {self.response}") 

                if request_command_number == MGR_ADD_ASSET:
                    asset_name = request[1]
                    asset_symbol = request[2]
                    asset_price = float(request[3])
                    asset_available_supply = int(request[4])
                    self.manager_add_asset(client, asset_name, asset_symbol, asset_price, asset_available_supply)
                
                if request_command_number == MGR_GET_ALL_ASSETS:
                    self.manager_get_all_assets(client)

                if request_command_number == MGR_REMOVE_ASSET:
                    asset_symbol = request[1]
                    self.manager_remove_asset(client, asset_symbol)

            else:
                # validates user request without the last element (id)
                is_command_valid = validate_user_request(request[:-1])

                if not is_command_valid:
                    self.response = [0, "Error: invalid command"]
                    print(f"SENT: {self.response}") 

                if request_command_number == USER_GET_ALL_ASSETS:
                    self.user_get_all_assets(client)
                
                if request_command_number == USER_GET_ASSETS_BALANCE:
                    self.user_get_assets_balance(client)

                if request_command_number == USER_BUY:
                    asset_symbol = request[1]
                    quantity = float(request[2])
                    self.user_buy_asset(client, asset_symbol, quantity)

                if request_command_number == USER_SELL:
                    asset_symbol = request[1]
                    quantity = float(request[2])
                    self.user_sell_asset(client, asset_symbol, quantity)

                if request_command_number == USER_DEPOSIT:
                    amount = float(request[1])
                    self.user_deposit(client, amount)

                if request_command_number == USER_WITHDRAW:
                    amount = float(request[1])
                    self.user_withdraw(client, amount)

            if self.response == False:
                self.response = [False]
            else:
                # if response was not a list or was an empty list, casts it into a list with the response inside
                if type(self.response) != list or (type(self.response) == list and len(self.response) == 0):
                    self.response = [self.response]
                if True not in self.response:
                    self.response.insert(0, True)

            self.response.insert(0, request_command_number+1)
            print(f"SENT: {self.response}") 
        except:
            return []
        
        return (self.response)
