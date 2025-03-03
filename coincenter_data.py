"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Número de aluno: 62220
"""
from typing import Dict
from abc import ABC, abstractmethod

MANAGER_SUPPORTED_COMMANDS = {
    1: "ADD_ASSET",
    2: "GET_ALL_ASSETS",
    3: "REMOVE_ASSET",
    0: "EXIT",
}

USER_SUPPORTED_COMMANDS = {
    1: "GET_ALL_ASSETS",
    2: "GET_BALANCE",
    3: "BUY",
    4: "SELL",
    5: "DEPOSIT",
    6: "WITHDRAW",
    0: "EXIT"
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
        # returns True if quantity is greater than 0 and not greater than available_supply
        return quantity > 0 and quantity <= self._available_supply

    def decrease_quantity(self, quantity:int) -> bool:
        if self.check_availability(quantity):
            self._available_supply -= quantity
            return True
        return False

    def increase_quantity(self, quantity):
        self._available_supply += quantity


class AssetController:
    assets:Dict[str, Asset] = {}

    @staticmethod
    def list_all_assets()->str:
        output = "ALL_ASSETS;"
        for asset in AssetController.assets.values():
            output += f"{asset.__str__()}:"
        output = output[:-1]
        return output
            
    @staticmethod
    def remove_asset(symbol:str):
        if symbol not in AssetController.assets.keys():
            print("Could not remove asset: asset does not exist.")
            return False
        del AssetController.assets[symbol]
        return True
    
    @staticmethod
    def add_asset(symbol:str,name:str,price:float,available_supply:int):
        if symbol in AssetController.assets.keys():
            print("Could not add asset: asset already exists.")
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
        output = f"BALANCE;€{self._balance};"
        for asset_symbol in self._holdings.keys():
            asset = AssetController.assets[asset_symbol]
            asset_string = str(asset.__str__())
            
            # gets the parameters without price and avaliable quantity of the asset
            asset_string = asset_string.split(";")[:2]
            
            # adds the symbol and name of asset to the response string
            for i in asset_string:
                output += f"{i};"
            
            # adds the quantity owned by user
            output += f"{self._holdings[asset_symbol]}:"
        output = output[:-1]
        return output

    def buy_asset(self, asset_symbol:str, quantity:float) -> bool:
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
        
    def deposite(self,amount):
        self._balance += amount
        return True

    def withdraw(self,amount):
        if amount <= self._balance:
            self._balance -= amount
            return True
        else:
            print("Could not withdraw: unavailable amount.")
            return False
           
    def process_request(self, request: str) -> str:
        result = ""
        request = request.split(";")
        command = request[0]
        
        if command == "GET_ALL_ASSETS":
            result = AssetController.list_all_assets()
            
        if command == "GET_BALANCE":
            result = self.__str__()
            
        if command == "BUY":
            was_bought = self.buy_asset(request[1], float(request[2]))
            result = was_bought
            
        if command == "SELL":
            was_sold = self.sell_asset(request[1], float(request[2]))
            result = was_sold
                
        if command == "DEPOSIT":
            was_deposited = self.deposite(float(request[1]))
            result = was_deposited
                
        if command == "WITHDRAW":
            was_withdrawn = self.withdraw(float(request[1]))
            result = was_withdrawn
        
        if result == True:
            result = "OK"
        elif result == False:
            result = "NOK"
         
        return result
        
        
class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    def process_request(self, request):
        result = ""
        request = request.split(";")
        command = request[0]    # gets the first index, which is the command itself
        
        if command == "ADD_ASSET":
            asset_name = request[1]
            asset_symbol = request[2]
            asset_price = float(request[3])
            asset_available_supply = float(request[4])
            
            was_asset_added = AssetController.add_asset(asset_symbol, asset_name, asset_price, asset_available_supply)
            result = f"OK;{asset_symbol}" if was_asset_added else "NOK"
                
        if command == "GET_ALL_ASSETS":
            result = AssetController.list_all_assets()
        
        if command == "REMOVE_ASSET":
            asset_symbol = request[1]
            was_asset_removed = AssetController.remove_asset(asset_symbol)
            result = f"OK;{asset_symbol}" if was_asset_removed else "NOK"
            
        return result

class ClientController:
    clients:Dict[int,Client] = {0:Manager(0)}

    @staticmethod
    def process_request(request:str) -> str:
        client_id = int(request.split(";")[-1])  # gets the id, which is the last arg in the request
        
        if client_id not in ClientController.clients.keys():
            ClientController.clients[client_id] = User(client_id)
        
        result = ClientController.clients[client_id].process_request(request)            
        return result