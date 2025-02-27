"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""
from typing import Dict,List
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
        pass

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
        output = ""
        for asset in AssetController.assets.values():
            output += f"{asset.__str__()}\n"
        return output
            
    @staticmethod
    def remove_asset(symbol:str):
        if symbol not in AssetController.assets.keys():
            print("Could not remove asset: asset does not exist.")
            return
        del AssetController.assets[symbol]

    @staticmethod
    def add_asset(symbol:str,name:str,price:float,available_supply:int):
        if symbol in AssetController.assets.keys():
            print("Could not add asset: asset already exists.")
            return
        
        # adds a new asset to the list of assets in the AssetController dict
        AssetController.assets[symbol] = Asset(symbol, name, price, available_supply)


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

    # TODO
    def __str__(self):
        pass

    def buy_asset(self, asset_symbol:str, quantity:float) -> bool:
        try:
            asset = AssetController.assets[asset_symbol]
            asset_bought = asset.decrease_quantity(quantity)
            
            if not asset_bought:
                print("Could not buy asset: quantity unavaiable")
            
            # if user already has this asset, increase the quantity,
            # else, creates a new entry in user's holdings for this asset
            elif asset_symbol in self._holdings.keys():
                self._holdings[asset_symbol] += quantity
            else:
                self._holdings[asset_symbol] = quantity
        except KeyError:
            print("Could not buy asset: asset does not exist")
            
    def sell_asset(self, asset_symbol:str, quantity:float) -> bool:
        try:
            if asset_symbol not in self._holdings.keys():
                print("Could not sell asset: User does not own this type of asset.")
                return
            
            if quantity < 0 or quantity > self._holdings[asset_symbol]:
                print("Could not sell asset: invalid quantity was given.")
                return 
             
            self._holdings[asset_symbol] -= quantity
            
            # increases the available quantity of this asset in the AssetController class
            asset = AssetController.assets[asset_symbol]
            asset.increase_quantity(quantity)  
        except KeyError:
            print("Could not sell asset: asset does not exist.")

    def deposite(self,amount):
        self._balance += amount

    def withdraw(self,amount):
        if amount <= self._balance:
            self._balance -= amount
        else:
            print("Could not withdraw: unavailable amount.")
           
    
    def process_request(self, request: str) -> str:
        response = ""
        request = request.split(";")
        
        # TODO fazer todos os tipos de request
        if request[0] == "GET_ALL_ASSETS":
            response += f"ALL_ASSETS;"
            for asset_symbol in self._holdings.keys():
                asset = AssetController.assets[asset_symbol]
                response += f"{asset.__str__()}:"
            response = response[:-1]
        if request[0] == "GET_BALANCE":
            response += f""


class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    # TODO
    def process_request(self, request):
        pass


class ClientController:
    clients:Dict[int,Client] = {0:Manager(0)}

    @staticmethod
    def process_request(request:str) -> str:
        client_id = request.split(";")[-1]  # gets the id, which is the last arg in the request
        
        if client_id not in ClientController.clients:
            ClientController.clients[client_id] = User(client_id)
        
        return ClientController.clients[client_id].process_request(request)            