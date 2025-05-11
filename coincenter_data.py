"""
Aplicações Distribuídas - Projeto 2 - coincenter_data.py
Número de aluno: 62220
"""

from abc import ABC
from setup_db import get_db

# constants with the number of each command

class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_supply:int):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.available_supply = available_supply

    # def __str__(self):
    #     result = f"{self._name};{self._symbol};{self._price};{self._available_supply}"
    #     return result

    def check_availability(self, quantity:int) -> bool:
        """
        Checks whether the asset is available in the given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if is available, False if it is not.
        """
        # returns True if quantity is greater than 0 and not greater than available_supply
        return quantity > 0 and quantity <= self.available_supply

    def decrease_available_supply(self, quantity:int) -> bool:
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if was completed, False if it was not.
        """
        if self.check_availability(quantity):
            self.available_supply -= quantity
            return True
        return False

    def increase_available_supply(self, quantity):
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if was completed, False if it was not.
        """
        if quantity > 0:
            self.available_supply += quantity
            

class Client(ABC):
    def __init__(self, id):
        self.id = id
    
    
class User(Client):
    def __init__(self, id, balance=0.0):
        super().__init__(id)
        if balance < 0:
            raise Exception("Balance cannot be lower than zero.")
        self.balance = 0.0

    def deposit(self, amount: float) -> bool:
        """
        Makes a deposit of the given amount.
        """
        if amount <= 0:
            print("Could not deposit: amount should be greater than 0.")
            return False
        self._balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
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

    def __str__(self):
        pass

           
class Manager(Client):
    def __init__(self, id):
        super().__init__(id)

    def create_new_asset(self, asset_name: str, asset_symbol: str, asset_price: float, asset_available_supply: int):
        """
        Adds an asset to the asset list
        """
        pass


class AssetController:

    @staticmethod
    def create_new_asset(symbol: str, name: str, price: float, available_supply: int) -> bool:
        asset = AssetRepository.get(symbol)
        if asset is None:
            asset = Asset(symbol, name, price, available_supply)
            AssetRepository.add(asset)
            return True
        return False

    @staticmethod
    def get_asset(symbol: str) -> dict:
        pass

    @staticmethod
    def get_all_assets() -> list:
        pass

class AssetRepository:
    @staticmethod
    def add(asset: Asset):
        db = get_db()
        cursor = db.cursor()
        query = "INSERT INTO Assets(asset_symbol, asset_name, price, available_supply)" \
        " VALUES (?, ?, ?, ?);"
        cursor.execute(query, (asset.symbol, asset.name, asset.price, asset.available_supply))

    @staticmethod
    def get(symbol: str):
        query = "SELECT * from Assets WHERE asset_symbol = ?"
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, (symbol))
        row = cursor.fetchone()
        if row is None:
            return None
        return Asset(
            row["asset_symbol"], row["asset_name"], row["price"], row["available_supply"]
        )

    @staticmethod
    def get_all():
        pass


class ClientController:
    @staticmethod
    def add_new_user(id: int) -> bool:
        pass

    @staticmethod
    def get_user_balance_assets(id: int) -> list:
        pass

    @staticmethod
    def get_client(id: int):
        pass

    @staticmethod
    def buy_asset(id:int, symbol: str) -> bool:
        pass

    @staticmethod
    def sell_asset(id:int, symbol: str) -> bool:
        pass

    @staticmethod
    def deposit(id: int, amount: float) -> bool:
        pass

    @staticmethod
    def withdraw(id: int, amount: float) -> bool:
        pass

    @staticmethod
    def transactions() -> str:
        pass

class ClientRepository:
    @staticmethod
    def add(client: Client):
        pass

    @staticmethod
    def get(id: int):
        pass

    @staticmethod
    def get_balance_assets(id: int):
        pass
