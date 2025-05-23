"""
Aplicações Distribuídas - Projeto 2 - coincenter_data.py
Número de aluno: 62220
"""

from abc import ABC
from setup_db import get_db
from flask import session
from datetime import datetime

# constants with the number of each command
ADD_ASSET = 1
GET_ALL_ASSETS = 2
GET_ASSET = 3

GET_ASSETS_BALANCE = 4
BUY = 5
SELL = 6
DEPOSIT = 7
WITHDRAW = 8
GET_TRANSACTIONS = 9

EXIT = 0

MANAGER_SUPPORTED_COMMANDS = {
    ADD_ASSET: "ADD_ASSET",
    GET_ALL_ASSETS: "GET_ALL_ASSETS",
    GET_ASSET: "GET_ASSET",
    GET_TRANSACTIONS: "GET_TRANSACTIONS",
    EXIT: "EXIT",
}

USER_SUPPORTED_COMMANDS = {
    GET_ALL_ASSETS: "GET_ALL_ASSETS",
    GET_ASSETS_BALANCE: "GET_ASSETS_BALANCE",
    BUY: "BUY",
    SELL: "SELL",
    DEPOSIT: "DEPOSIT",
    WITHDRAW: "WITHDRAW",
    EXIT: "EXIT"
}

class AssetAlreadyExistsException(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 409

class InvalidAmountException(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 409

class NotFoundException(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 404
        
class NotEnoughBalanceException(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 406

class AssetNotEnoughQuantityException(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 409

class ClientNotEnoughAsset(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 409

class NotManagerException(Exception):
    def __init__(self, message, detail):
        super().__init__(message)
        self.title = message
        self.detail = detail
        self.code = 403


class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_quantity:float):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.available_quantity = available_quantity

    def check_availability(self, quantity:float) -> bool:
        """
        Checks whether the asset is available in the given quantity.
        
        Requires:
        - quantity float
        
        Ensures:
        True if is available, False if it is not.
        """
        # returns True if quantity is greater than 0 and not greater than available_quantity
        return quantity > 0 and quantity <= self.available_quantity

    def decrease_available_quantity(self, quantity:float) -> bool:
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity float
        
        Ensures:
        True if was completed, False if it was not.
        """
        if self.check_availability(quantity):
            self.available_quantity -= quantity
            return True
        return False

    def increase_available_quantity(self, quantity: float):
        """
        Decreases the amount of the asset in a given quantity.
        
        Requires:
        - quantity float
        
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
        self.balance = balance

    def buy_asset(self, quantity: float, asset: Asset) -> bool:
        asset_price = asset.price
        if self.balance < quantity * asset_price:
            return False
        self.balance -= quantity * asset_price
        return True
    
    def sell_asset(self, quantity: float, asset: Asset):
        asset_price = asset.price
        self.balance += quantity * asset_price

    def deposit(self, amount: float) -> bool:
        """
        Makes a deposit of the given amount.
        """
        if amount <= 0:
            print("Could not deposit: amount should be greater than 0.")
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws the given amount.
        """
        if amount <= 0:
            print("Could not withdraw: amount should be greater than 0.")
            return False
        if amount > self.balance:
            print("Could not withdraw: unavailable amount.")
            return False
        
        self.balance -= amount
        return True

           
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
            raise AssetAlreadyExistsException("Asset already exists.", "There is already an asset with this symbol.")

        asset = Asset(symbol, name, price, available_quantity)
        AssetRepository.add(asset)

    @staticmethod
    def get_asset(symbol: str) -> dict:
        asset = AssetRepository.get(symbol)
        if asset is None:
            raise NotFoundException("Asset not found.", "There is not an asset with this symbol.")
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
            raise NotFoundException("Assets not found.", "There are no assets registered in the system.")
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
    
    @staticmethod
    def update_available_quantity(symbol: str, quantity: float):
        db = get_db()
        cursor = db.cursor()

        query = "UPDATE Assets SET available_quantity = ? WHERE asset_symbol = ?;"
        cursor.execute(query, (quantity, symbol))
        db.commit()


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
            
        session['client_id'] = id
        session.modified = True
    
    @staticmethod
    def get_user_balance_assets(id: int) -> dict:
        client = ClientRepository.get(id)

        if isinstance(client, User):
            balance = client.balance
            user_assets = AssetRepository.get_by_user_id(id)
            return {
                "balance" : balance,
                "assets" : 
                    [{
                        "symbol" : a.symbol,
                        "name" : a.name,
                        "price" : a.price,
                        "available_quantity" : a.available_quantity
                    } for a in user_assets ] 
                    if user_assets is not None else "No assets"
            }

        return None

    @staticmethod
    def buy_asset(id:int, symbol: str, quantity: float) -> bool:
        client = ClientRepository.get(id)
        asset = AssetRepository.get(symbol)

        if asset is None:
            raise NotFoundException("Asset not found.", "There is not an asset with this symbol.")
        
        if isinstance(client, User):
            if not client.buy_asset(quantity, asset):
                raise NotEnoughBalanceException("Not enough balance.", "Your balance is not enough to buy this quantity of this asset.")
            if not asset.decrease_available_quantity(quantity):
                raise AssetNotEnoughQuantityException("Quantity unavailable.", "This asset is not available in this quantity.")
            
            AssetRepository.update_available_quantity(symbol, asset.available_quantity)
            ClientRepository.update_balance(id, client.balance)
            ClientRepository.buy_asset(id, symbol, quantity)

            current_datetime = datetime.now()
            current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            ClientRepository.add_transaction(id, symbol, "BUY", quantity, quantity*asset.price, current_datetime_formatted)

            return True

    @staticmethod
    def sell_asset(id:int, symbol: str, quantity: float) -> bool:
        client = ClientRepository.get(id)
        asset = AssetRepository.get(symbol)

        if asset is None:
            raise NotFoundException("Asset not found.", "There is not an asset with this symbol.")
        
        if isinstance(client, User):
            ClientRepository.sell_asset(id, symbol, quantity)
            
            asset.increase_available_quantity(quantity)
            AssetRepository.update_available_quantity(symbol, asset.available_quantity)
            
            client.sell_asset(quantity, asset)
            ClientRepository.update_balance(id, client.balance)

            current_datetime = datetime.now()
            current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            ClientRepository.add_transaction(id, symbol, "SELL", quantity, quantity*asset.price, current_datetime_formatted)

            return True

    @staticmethod
    def deposit(id: int, amount: float) -> bool:
        client = ClientRepository.get(id)
        
        if isinstance(client, User):
            if not client.deposit(amount):
                raise InvalidAmountException("Invalid amount to deposit", "Value should be greater than 0.")
            
            ClientRepository.update_balance(id, client.balance)
            return True

    @staticmethod
    def withdraw(id: int, amount: float) -> bool:
        client = ClientRepository.get(id)

        if isinstance(client, User):
            if not client.withdraw(amount):
                raise InvalidAmountException("Invalid amount to withdraw", "Amount should be greater than 0 and you should have enough balance to withdraw.")
            
            ClientRepository.update_balance(id, client.balance)
            return True

    @staticmethod
    def get_transactions(requester_id: int) -> list:

        requester = ClientRepository.get(requester_id)
        if not isinstance(requester, Manager):
            raise NotManagerException("Forbidden.", "Resource only accessible by managers.")

        transactions_list = ClientRepository.get_transactions()

        if transactions_list is None:
            raise NotFoundException("Transactions not found.", "There are no transactions.")
        return [
            {
                "id" : t["id"],
                "client id" : t["client_id"],
                "asset symbol" : t["asset_symbol"],
                "type" : t["type"],
                "quantity" : t["quantity"],
                "price" : t["price"],
                "time" : t["time"]
            } 
            for t in transactions_list
        ]


        


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
        
        print("row balance = ", row["balance"])
        return User(row["client_id"], row["balance"])

    @staticmethod
    def update_balance(id: int, balance: float):
        db = get_db()
        cursor = db.cursor()

        query = "UPDATE Clients SET balance = ? WHERE client_id = ?;"
        cursor.execute(query, (balance, id))
        db.commit()
        
    @staticmethod
    def buy_asset(id: int, asset_symbol: str, quantity: float):
        db = get_db()
        cursor = db.cursor()

        query_already_has_asset = "SELECT * FROM ClientAssets WHERE client_id = ? " \
        "AND asset_symbol = ?;"
        cursor.execute(query_already_has_asset, (id, asset_symbol))
        row = cursor.fetchone()

        if row == None:
            query = "INSERT INTO ClientAssets(client_id, asset_symbol, quantity) " \
            "VALUES (?, ?, ?);"
            cursor.execute(query, (id, asset_symbol, quantity))
            db.commit()
        else:
            query = "UPDATE ClientAssets SET quantity = quantity + ? WHERE client_id = ? " \
            "AND asset_symbol = ?;"
            cursor.execute(query, (quantity, id, asset_symbol))
            db.commit()

    @staticmethod
    def sell_asset(id: int, asset_symbol: str, quantity: float):
        db = get_db()
        cursor = db.cursor()

        query_already_has_asset = "SELECT * FROM ClientAssets WHERE client_id = ? " \
        "AND asset_symbol = ?;"
        cursor.execute(query_already_has_asset, (id, asset_symbol))
        row = cursor.fetchone()

        if row == None:
            raise ClientNotEnoughAsset("You do not own this asset.")
        
        if row["quantity"] - quantity < 0:
            raise ClientNotEnoughAsset("The quantity you own of this asset is not enough.")
        if row["quantity"] - quantity == 0:
            query = "DELETE FROM ClientAssets WHERE client_id = ? " \
            "AND asset_symbol = ?"
            cursor.execute(query, (id, asset_symbol))
        else:
            query = "UPDATE ClientAssets SET quantity = quantity - ? WHERE client_id = ? " \
            "AND asset_symbol = ?;"
            cursor.execute(query, (quantity, id, asset_symbol))
            
        db.commit()

    @staticmethod
    def add_transaction(client_id: int, asset_symbol: str, transaction_type: str, quantity: float, price: float, current_date: str):
        db = get_db()
        cursor = db.cursor()

        query = "INSERT INTO Transactions(id, client_id, asset_symbol, type, quantity, price, time)" \
        " VALUES (NULL, ?, ?, ?, ?, ?, ?);"

        cursor.execute(query, (client_id, asset_symbol, transaction_type, quantity, price, current_date))
        db.commit()

    @staticmethod
    def get_transactions() -> list:
        db = get_db()
        cursor = db.cursor()

        query = "SELECT * FROM Transactions;"
        cursor.execute(query)
        rows = cursor.fetchall()

        if len(rows) == 0:
            return None
        
        return rows
