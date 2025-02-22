"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Grupo: XX
Números de aluno: XXXXX XXXXX
"""
from typing import Dict,List
from abc import ABC, abstractmethod

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
    assets:Dict[Asset] = {}

    @staticmethod
    def list_all_assets()->str:
        output = ""
        for asset in AssetController.assets.values():
            output += f"{asset.__str__()}\n"
        return output
            
    @staticmethod
    def remove_asset(symbol:str):
        if symbol not in AssetController.assets.keys():
            print("Couldn't remove asset: asset does not exist")
            return
        del AssetController.assets[symbol]

    @staticmethod
    def add_asset(symbol:str,name:str,price:float,available_supply:int):
        if symbol in AssetController.assets.keys():
            print("Couldn't add asset: asset already exists")
            return
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
                print("Couldn't buy asset: quantity unavaiable")
            else:
                self._holdings[asset._symbol] = quantity
        except KeyError:
            print("Couldn't buy asset: asset does not exist")
            
    def sell_asset(self, asset_symbol:str, quantity:float) -> bool:
        try:
            if asset_symbol not in self._holdings.keys():
                print("Couldn't sell asset: User does not own this type of asset")
                return
            
            asset = AssetController.assets[asset_symbol]
            if quantity < 0 or quantity > self._holdings[asset_symbol]:
                print("Couldn't sell asset: invalid quantity was given")
                return 
             
            self._holdings[asset_symbol] -= quantity
            asset.increase_quantity(quantity)  
        except KeyError:
            print("Couldn't sell asset: asset does not exist")

    def deposite(self,amount):
        self._balance += amount

    def withdraw(self,amount):
        if amount <= self._balance:
            self._balance -= amount
    
    def process_request(self, request) -> str:
        pass

class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    def process_request(self, request):
        pass

class ClientController:
    clients:Dict[int,Client] = {0:Manager(0)}

    @staticmethod
    def process_request(request:str)->str:
        ### código ###
        client_id = ...
        
        if client_id not in ClientController.clients:
            ClientController.clients[id] = User(id)
        
        return ClientController.clients[client_id].process_request(request)            