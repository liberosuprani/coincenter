from coincenter_data import *

class CoincenterSkeleton:
    def __init__(self):
        self.response = []

    def manager_add_asset(self, asset_name, asset_symbol, asset_price, asset_available_supply):
        self.response = Manager.add_asset(asset_name, asset_symbol, asset_price, asset_available_supply)
        
    def manager_get_all_assets(self):
        self.response = Manager.get_all_assets()

    def manager_remove_asset(self, asset_symbol):
        self.response = Manager.remove_asset(asset_symbol)

    def user_get_all_assets(self):
        self.response = User.get_all_assets()

    def user_get_assets_balance(self):
        self.response = User.get_assets_balance()

    def user_buy_asset(self, asset_symbol, quantity):
        self.response = User.buy_asset(asset_symbol, quantity)

    def user_sell_asset(self, asset_symbol, quantity):
        self.response = User.sell_asset(asset_symbol, quantity)

    def user_deposit(self, amount):
        self.response = User.deposit(amount)

    def user_withdraw(self, amount):
        self.response = User.withdraw(amount)

    def process_request(self, request) -> tuple[int, list]:
        try:
            request_command_number = request[0]
            request_id = request[-1]

            print(request)
            
            if request_command_number == USER_EXIT or request_command_number == MGR_EXIT:
                self.response = [request_command_number+1, True]
            
            elif request_id == 0:
                if request_command_number == MGR_ADD_ASSET:
                    asset_name = request[1]
                    asset_symbol = request[2]
                    asset_price = request[3]
                    asset_available_supply = request[4]
                    self.manager_add_asset(asset_name, asset_symbol, asset_price, asset_available_supply)
                
                if request_command_number == MGR_GET_ALL_ASSETS:
                    self.manager_get_all_assets()

                if request_command_number == MGR_REMOVE_ASSET:
                    asset_symbol = request[1]
                    self.manager_remove_asset(asset_symbol)

            else:
                if request_command_number == USER_GET_ALL_ASSETS:
                    self.user_get_all_assets()
                
                if request_command_number == USER_GET_ASSETS_BALANCE:
                    self.user_get_assets_balance()

                if request_command_number == USER_BUY:
                    asset_symbol = request[1]
                    quantity = request[2]
                    self.user_buy_asset(asset_symbol, quantity)

                if request_command_number == USER_SELL:
                    asset_symbol = request[1]
                    quantity = request[2]
                    self.user_sell_asset(asset_symbol, quantity)

                if request_command_number == USER_DEPOSIT:
                    amount = request[1]
                    self.user_deposit(amount)

                if request_command_number == USER_WITHDRAW:
                    amount = request[1]
                    self.user_withdraw(amount)

            if self.response == False:
                self.response = [False]

            self.response.insert(0, request_command_number+1)

            print(f"SENT: {self.response}") 
        except:
            return []
        
        return (self.response)
