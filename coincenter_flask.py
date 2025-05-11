"""
Aplicações Distribuídas - Projeto 2 - coincenter_server.py
Número de aluno: 62220
"""

from flask import Flask, request, g
import json
from coincenter_data import AssetController, ClientController
from setup_db import connect_db

app = Flask(__name__)

@app.route("/asset", methods = ["POST"])
@app.route("/asset/<str:symbol>", methods = ["GET"])
def asset(symbol=None):
    g.db, g.cursor = connect_db()

    if request.method == "GET":
        response = AssetController.get_asset(symbol)
        return response

    if request.method == "POST":
        request_data = json.loads(request.data)
        symbol = request_data["symbol"]
        name = request_data["name"]
        price = request_data["price"]
        available_supply = request_data["available_supply"]
        response = AssetController.create_new_asset(
            symbol, name, price, available_supply
        )
        
        return response
    

@app.route("/assetset", methods = ["GET"])
def asset_set():
    g.db, g.cursor = connect_db()
    response = AssetController.get_all_assets()
    return response


@app.route("/login/", methods = ["POST"])
def login(id):
    g.db, g.cursor = connect_db()
    response = ClientController.add_new_client(id)
    return response


@app.route("/user<int:id>", methods = ["GET"])
def user(id):
    g.db, g.cursor = connect_db()
    response = ClientController.get_user_balance_assets(id)
    return response


@app.route("/buy", methods = ["POST"])
def buy_asset(id, symbol):
    g.db, g.cursor = connect_db()
    response = ClientController.buy_asset(id, symbol)
    return response


@app.route("/sell", methods = ["POST"])
def sell_asset(id, symbol):
    g.db, g.cursor = connect_db()
    response = ClientController.sell_asset(id, symbol)
    return response


@app.route("/deposit", methods = ["POST"])
def deposit(id, amount):
    g.db, g.cursor = connect_db()
    response = ClientController.deposit(id, amount)
    return response


@app.route("/withdraw", methods = ["POST"])
def withdraw(id, amount):
    g.db, g.cursor = connect_db()
    response = ClientController.withdraw(id, amount)
    return response


@app.route("/transactions", methods = ["GET"])
def transactions(id):
    g.db, g.cursor = connect_db()
    response = ClientController.transactions()
    return response
    

if __name__ == "__main__":
    app.run()

