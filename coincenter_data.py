"""
Aplicações Distribuídas - Projeto 2 - coincenter_data.py
Número de aluno: 62220
"""

from abc import ABC
from setup_db import get_db
from flask import session

# constants with the number of each command

class AssetAlreadyExistsException(Exception):
    pass
class InvalidAssetSymbol(Exception):
    pass
class AssetNotFoundException(Exception):
    pass
class NotEnoughBalanceException(Exception):
    pass
class AssetNotEnoughQuantityException(Exception):
    pass


class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_quantity:int):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.available_quantity = available_quantity

    def check_availability(self, quantity:int) -> bool:
        """
        Checks whether the asset is available in the given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if is available, False if it is not.
        """
        # returns True if quantity is greater than 0 and not greater than available_quantity
        return quantity > 0 and quantity <= self.available_quantity

    def decrease_available_quantity(self, quantity:int) -> bool:
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if was completed, False if it was not.
        """
        if self.check_availability(quantity):
            self.available_quantity -= quantity
            return True
        return False

    def increase_available_quantity(self, quantity):
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity int
        
        Ensures:
        True if was completed, False if it was not.
        """
        if quantity > 0:
            self.available_quantity += quantity
            

class Client(ABC):
    def __init__(self, id):
        self.id = id
    
    
class User(Client):
    def __init__(self, id, balance=0.0):
        super().__init__(id)
        if balance < 0:
            raise Exception("Balance cannot be lower than zero.")
        self.balance = 0.0

    # TODO
    def buy_asset(quantity: float, asset: Asset) -> bool:
        pass

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

    def create_new_asset(self, asset_name: str, asset_symbol: str, asset_price: float, asset_available_quantity: int):
        """
        Adds an asset to the asset list
        """
        pass


class AssetController:

    @staticmethod
    def create_new_asset(symbol: str, name: str, price: float, available_quantity: int):
        asset = AssetRepository.get(symbol)

        if asset is not None:
            raise AssetAlreadyExistsException("There is already an asset with this symbol")

        asset = Asset(symbol, name, price, available_quantity)
        AssetRepository.add(asset)

    @staticmethod
    def get_asset(symbol: str) -> dict:
        asset = AssetRepository.get(symbol)
        if asset is None:
            raise AssetNotFoundException("There is not an asset with this symbol.")
        return {
            "symbol" : asset.symbol,
            "name" : asset.name,
            "price" : asset.price,
            "available_quantity" : asset.available_quantity
        }

    @staticmethod
    def get_all_assets() -> list:
        asset_list = AssetRepository.get_all()

        if asset_list is None:
            raise AssetNotFoundException("There are no assets registered in the system.")
        return [
            {
                "symbol" : a.symbol,
                "name" : a.name,
                "price" : a.price,
                "available_quantity" : a.available_quantity
            }
            for a in asset_list
        ]

class AssetRepository:
    @staticmethod
    def add(asset: Asset):
        db = get_db()
        cursor = db.cursor()
        
        query = "INSERT INTO Assets(asset_symbol, asset_name, price, available_quantity)" \
        " VALUES (?, ?, ?, ?);"
        cursor.execute(query, (asset.symbol, asset.name, asset.price, asset.available_quantity))
        db.commit()

    @staticmethod
    def get(symbol: str) -> Asset:
        db = get_db()
        cursor = db.cursor()

        query = "SELECT * from Assets WHERE asset_symbol = ?"
        cursor.execute(query, (symbol,))
        row = cursor.fetchone()

        if row is None:
            return None
        return Asset(
            row["asset_symbol"], row["asset_name"], row["price"], row["available_quantity"]
        )

    @staticmethod
    def get_all() -> list:
        db = get_db()
        cursor = db.cursor()

        query = "SELECT * FROM Assets"
        cursor.execute(query)
        rows = cursor.fetchall()

        asset_list = []
        if len(rows) == 0:
            return None
        for row in rows:
            asset = Asset(row["asset_symbol"], row["asset_name"], row["price"], row["available_quantity"])
            asset_list.append(asset)
        return asset_list

    @staticmethod
    def get_by_user_id(id: int) -> list:
        db = get_db()
        cursor = db.cursor()

        query = "SELECT asset_symbol FROM ClientAssets WHERE client_id = ?"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()

        asset_list = []
        if len(rows) == 0:
            return None
        for row in rows:
            asset = AssetRepository.get(row["asset_symbol"])
            asset_list.append(asset)
        return asset_list


class ClientController:

    @staticmethod
    def login(id: int):
        client = ClientRepository.get(id)   

        if client is None:
            if id == 0:
                client = Manager(id)
            else:
                client = User(id)
            ClientRepository.add(client)
            
        session["client_id"] = id
    
    @staticmethod
    def get_user_balance_assets(id: int) -> dict:
        client = ClientRepository.get(id)

        if isinstance(client, User):
            balance = client.balance
            user_assets = AssetRepository.get_by_user_id(id)
            return {
                "balance" : balance,
                "assets" : user_assets if user_assets is not None else "No assets"
            }

        return None

    @staticmethod
    def buy_asset(id:int, symbol: str, quantity: int) -> bool:
        client = ClientRepository.get(id)
        asset = AssetRepository.get(symbol)

        if asset is None:
            raise AssetNotFoundException("There is not an asset with this symbol.")
        
        if isinstance(client, User):
            if not client.buy_asset(quantity, asset):
                raise NotEnoughBalanceException("Not enough balance.")
            if not asset.decrease_available_quantity(quantity):
                raise AssetNotEnoughQuantityException("Asset is not available in this quantity.")
            
            AssetRepository.update_available_quantity(symbol, asset.available_quantity)
            ClientRepository.update_balance(id, client.balance)
            ClientRepository.add_asset(id, symbol)

            return True

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
        db = get_db()
        cursor = db.cursor()

        if isinstance(client, Manager):
            query = "INSERT INTO Clients(client_id, is_manager) VALUES (?, ?);"
            cursor.execute(query, (client.id, 1))
        else:
            query = "INSERT INTO Clients(client_id, is_manager, balance) VALUES (?, ?, ?);"
            cursor.execute(query, (client.id, 0, client.balance))
        
        db.commit()

    @staticmethod
    def get(id: int) -> Client:
        db = get_db()
        cursor = db.cursor()

        query = "SELECT * from Clients WHERE client_id = ?;"
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row == None:
            return None
        
        if row["is_manager"] == 1:
            return Manager(row["client_id"])
        
        return User(row["client_id"], row["balance"])

    #TODO
    @staticmethod
    def update_balance(id: int, balance: float):
        pass

        