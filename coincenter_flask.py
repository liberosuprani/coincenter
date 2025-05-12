"""
Aplicações Distribuídas - Projeto 2 - coincenter_server.py
Número de aluno: 62220
"""

from flask import Flask, request, make_response, session
import json
from coincenter_data import AssetController, ClientController

app = Flask(__name__)
app.secret_key = "chave secreta"

@app.route("/asset", methods = ["POST"])
@app.route("/asset/<string:symbol>", methods = ["GET"])
def asset():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    if request.method == "GET":
        response = AssetController.get_asset(symbol)
        if response:
            r.status_code = 200
            r.data = json.dumps(response)
        else:
            r.data = json.dumps({
                "title" : "There is not an asset with this symbol.",
                "status" : 404
            })

    if request.method == "POST":
        try:
            req = request.get_json()
            symbol = req["symbol"]
            name = req["name"]
            price = req["price"]
            available_quantity = req["available_quantity"]
        except KeyError:
            r.status_code = 400
            r.data = json.dumps({
                "title" : "There were missing arguments for the creation of the asset.",
                "status" : 400
            })
            return r

        response = AssetController.create_new_asset (
            symbol, name, price, available_quantity
        )

        if response:
            r.data = json.dumps({
                "title" : "Asset was created successfully.",
                "status" : 201

            })
        else:
            r.data = json.dumps({
                "title" : "There is already an asset with this symbol.",
                "status" : 409,
            })
        
    return r
    

@app.route("/assetset", methods = ["GET"])
def asset_set():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    response = AssetController.get_all_assets()

    if response:
        r.status_code = 200
        r.data = json.dumps(response)
    else:
        r.data = json.dumps({
            "title" : "There are no assets registered in the system.",
            "status" : 404
        })
    return r


@app.route("/login", methods = ["POST"])
def login():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    req = request.get_json()
    client_id = req["client_id"]
    
    response = ClientController.login(client_id)
    if response:
        r.status_code = 200
    return r

# @app.route("/user<int:id>", methods = ["GET"])
# def user(id):
#     response = ClientController.get_user_balance_assets(id)
#     return response


# @app.route("/buy", methods = ["POST"])
# def buy_asset(id, symbol):
#     response = ClientController.buy_asset(id, symbol)
#     return response


# @app.route("/sell", methods = ["POST"])
# def sell_asset(id, symbol):
#     response = ClientController.sell_asset(id, symbol)
#     return response


# @app.route("/deposit", methods = ["POST"])
# def deposit(id, amount):
#     response = ClientController.deposit(id, amount)
#     return response


# @app.route("/withdraw", methods = ["POST"])
# def withdraw(id, amount):
#     response = ClientController.withdraw(id, amount)
#     return response


# @app.route("/transactions", methods = ["GET"])
# def transactions(id):
#     response = ClientController.transactions()
#     return response
    

if __name__ == "__main__":
    app.run()

