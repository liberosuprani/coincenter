"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Número de aluno: 62220
"""
from typing import Dict
from abc import ABC, abstractmethod

# constants with the number of each command
MGR_ADD_ASSET = 10
MGR_GET_ALL_ASSETS = 20
MGR_REMOVE_ASSET = 30
MGR_EXIT = 40
USER_GET_ALL_ASSETS = 50
USER_GET_ASSETS_BALANCE = 60
USER_BUY = 70
USER_SELL = 80
USER_DEPOSIT = 90
USER_WITHDRAW = 100
USER_EXIT = 110

MANAGER_SUPPORTED_COMMANDS = {
    MGR_ADD_ASSET: "ADD_ASSET",
    MGR_GET_ALL_ASSETS: "GET_ALL_ASSETS",
    MGR_REMOVE_ASSET: "REMOVE_ASSET",
    MGR_EXIT: "EXIT",
}

USER_SUPPORTED_COMMANDS = {
    USER_GET_ALL_ASSETS: "GET_ALL_ASSETS",
    USER_GET_ASSETS_BALANCE: "GET_ASSETS_BALANCE",
    USER_BUY: "BUY",
    USER_SELL: "SELL",
    USER_DEPOSIT: "DEPOSIT",
    USER_WITHDRAW: "WITHDRAW",
    USER_EXIT: "EXIT"
}

class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_supply:int):
        self._symbol = symbol
        self._name = name
        self._price = price
        self._available_supply = available_supply

    def __str__(self):
        result = f"{self._name};{self._symbol};{self._price};{self._available_supply}"
        return result

    def check_availability(self, quantity:int) -> bool:
        """
        Checks whether the asset is available in the given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if is available, False if it is not.
        """
        # returns True if quantity is greater than 0 and not greater than available_supply
        return quantity > 0 and quantity <= self._available_supply

    def decrease_quantity(self, quantity:int) -> bool:
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if was completed, False if it was not.
        """
        if self.check_availability(quantity):
            self._available_supply -= quantity
            return True
        return False

    def increase_quantity(self, quantity):
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if was completed, False if it was not.
        """
        if quantity > 0:
            self._available_supply += quantity
            

class AssetController:
    assets:Dict[str, Asset] = {}

    @staticmethod
    def list_all_assets() -> str:
        """
        Lists all the assets.
        """
        output = []
        for asset in AssetController.assets.values():
            output.append(asset.__str__())
        return output
            
    @staticmethod
    def remove_asset(symbol:str) -> bool:
        """
        Removes an asset based on the given symbol
        
        Requires:
        - symbol str
        
        Ensures:
        Deletion and True if it was completed, False if it was not.
        """
        if symbol not in AssetController.assets.keys():
            print("Could not remove asset: asset does not exist.")
            return False
        
        # if a user has this asset, then does not remove it
        clients = ClientController.clients
        for id in clients.keys():
            if id != 0:
                if symbol in clients[id]._holdings.keys():
                    print("Could not remove asset: a user has this asset.")
                    return False
                
        del AssetController.assets[symbol]
        return True
    
    @staticmethod
    def add_asset(symbol:str, name:str, price:float, available_supply:int) -> bool:
        """
        Adds an asset.
        
        Requires:
        - symbol str
        - name str
        - price float
        - available_supply int
        
        Ensures:
        The addition and True if it was completed, False if it was not.
        """
        if symbol in AssetController.assets.keys():
            print("Could not add asset: asset already exists.")
            return False
        
        if price <= 0:
            print("Could not add asset. Price should be greater than 0.")
            return False
        if available_supply <= 0:
            print("Could not add asset. Available amount should be greater than 0.")
            return False
        
        # adds a new asset to the list of assets in the AssetController dict
        AssetController.assets[symbol] = Asset(symbol, name, price, available_supply)
        return True


class Client(ABC):
    def __init__(self, id):
        self.id = id
    
    @abstractmethod
    def process_request(self,_):
        pass
    
    
class User(Client):
    def __init__(self, user_id):
        super().__init__(user_id)
        self._balance = 0.0
        self._holdings: Dict[str, float] = {}

    def __str__(self):
        output = [self._balance]
        
        for asset_symbol in self._holdings.keys():
            asset = AssetController.assets[asset_symbol]
            asset_string = str(asset.__str__())
            
            # gets the parameters without price and avaliable quantity of the asset
            asset_string_aux = asset_string.split(";")[:2]

            # adds the quantity owned by user
            asset_string_aux.append(self._holdings[asset_symbol])
            
            asset_string = ""
            for element in asset_string_aux:
                asset_string += f"{element};"

            asset_string = asset_string[:-1]

            output.append(asset_string)
        return output

    def buy_asset(self, asset_symbol:str, quantity:float) -> bool:
        """
        Buys an asset.
        """
        try:
            asset = AssetController.assets[asset_symbol]
            
            # user doesnt have enough balance to buy this quantity of asset
            if self._balance < asset._price * quantity:
                print("Could not buy asset: not enough balance.")
                return False
            
            was_asset_bought = asset.decrease_quantity(quantity)
            
            # asset is not available in this quantity
            if not was_asset_bought:
                print("Could not buy asset: quantity unavaiable.")
                return False
            
            # if user already has this asset, increase the quantity,
            # else, creates a new entry in user's holdings for this asset
            elif asset_symbol in self._holdings.keys():
                self._holdings[asset_symbol] += quantity
            else:
                self._holdings[asset_symbol] = quantity
                
            # decreases the balance according to the amount of this asset
            # that was bought
            self._balance -= asset._price*quantity
            
            return True
        except KeyError:
            print("Could not buy asset: asset does not exist.")
            return False
            
    def sell_asset(self, asset_symbol:str, quantity:float) -> bool:
        """
        Sells an asset.
        """
        try:
            if asset_symbol not in self._holdings.keys():
                print("Could not sell asset: user does not own this type of asset.")
                return False
            
            if quantity < 0 or quantity > self._holdings[asset_symbol]:
                print("Could not sell asset: invalid quantity was given.")
                return False
            
            self._holdings[asset_symbol] -= quantity
            
            asset = AssetController.assets[asset_symbol]
            
            # increases the user's balance according to the amount sold
            self._balance += asset._price * quantity
            
            # remove asset entry in the table if the quantity owned is 0
            if self._holdings[asset_symbol] == 0:
                del self._holdings[asset_symbol]
            
            # increases the available quantity of this asset in the AssetController class
            asset.increase_quantity(quantity)  
            return True
        except KeyError:
            print("Could not sell asset: asset does not exist.")
            return False
        
    def deposit(self, amount) -> bool:
        """
        Makes a deposit of the given amount.
        """
        if amount <= 0:
            print("Could not deposit: amount should be greater than 0.")
            return False
        self._balance += amount
        return True

    def withdraw(self, amount) -> bool:
        """
        Withdraws the given amount.
        """
        if amount <= 0:
            print("Could not withdraw: amount should be greater than 0.")
            return False
        if amount <= self._balance:
            self._balance -= amount
            return True
        else:
            print("Could not withdraw: unavailable amount.")
            return False
           
    def process_request(self, request: list) -> list:
        """
        Processes the request given and gives a response.
        """
        
        command = request[0]
        result = [command+1]

        if command == USER_GET_ALL_ASSETS: # get all assets
            result.extend(AssetController.list_all_assets())

            # the list of all assets returned was an empty list
            if len(result) == 1:
                result.append(False)
                
        if command == USER_GET_ASSETS_BALANCE: # get assets balance
            try:
                result.extend(self.__str__())
            except:
                result.append(False)
                
        if command == USER_BUY: # buy asset
            was_bought = self.buy_asset(request[1], float(request[2]))
            result.append(was_bought)
            
        if command == USER_SELL: # sell asset
            was_sold = self.sell_asset(request[1], float(request[2]))
            result.append(was_sold)
                
        if command == USER_DEPOSIT: # deposit
            was_deposited = self.deposit(float(request[1]))
            result.append(was_deposited)
                
        if command == USER_WITHDRAW: # withdraw
            was_withdrawn = self.withdraw(float(request[1]))
            result.append(was_withdrawn)
        
        # if result[1] is a boolean, response is the same
        # else, it means that result[1] is the result of an operation (e.g. list all assets)
        # then, insert True into index 1
        response = result

        if result[1] == True or result[1] == False:
            response = result
        else:
            response.insert(1, True)

        return response
        
        
class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    def process_request(self, request: list) -> list:
        """
        Processes the request given and gives a response.
        """
        
        command = request[0]    # gets the first index, which is the command itself
        result = [command+1]
        
        if command == MGR_ADD_ASSET: # add asset
            asset_name = request[1]
            asset_symbol = request[2]
            asset_price = float(request[3])
            asset_available_supply = float(request[4])
            
            was_asset_added = AssetController.add_asset(asset_symbol, asset_name, asset_price, asset_available_supply)
            result.append(was_asset_added)
                
        if command == MGR_GET_ALL_ASSETS: # list all assets
            result.extend(AssetController.list_all_assets())
            
            # the list of all assets returned was an empty list
            if len(result) == 1:
                result.append(False)
                
        if command == MGR_REMOVE_ASSET: # remove asset
            asset_symbol = request[1]
            was_asset_removed = AssetController.remove_asset(asset_symbol)
            result.append(was_asset_removed)

            if was_asset_removed:
                result.append(asset_symbol)
            
        return result

class ClientController:
    clients:Dict[int,Client] = {0:Manager(0)}

    @staticmethod
    def process_request(request:list) -> list:
        client_id = int(request[-1])  # gets the id, which is the last element in the request
        
        if client_id not in ClientController.clients.keys():
            ClientController.clients[client_id] = User(client_id)
        
        result = ClientController.clients[client_id].process_request(request)            
        return result