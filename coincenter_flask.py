"""
Aplicações Distribuídas - Projeto 2 - coincenter_server.py
Número de aluno: 62220
"""

from flask import Flask, request, make_response, session
import json
from coincenter_data import *
import coincenter_data as exceptions

app = Flask(__name__)
app.secret_key = "chave secreta"

def return_not_authenticated_error():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    if "client_id" not in session:
        r.status_code = 401
        r.data = json.dumps({
            "title" : "Not logged in.",
            "status" : 401
        })
        return r
    
    return False


@app.route("/asset", methods = ["POST"])
@app.route("/asset/<string:symbol>", methods = ["GET"])
def asset(symbol=None):
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    if request.method == "GET":
        try:
            response = AssetController.get_asset(symbol)
            r.status_code = 200
            r.data = json.dumps(response)
        except exceptions.AssetNotFoundException as e:
            r.status_code = 404
            r.data = json.dumps({
                "title" : str(e),
                "status" : 404
            })

    if request.method == "POST":
        try:
            req = request.get_json()
            symbol = req["symbol"]
            name = req["name"]
            price = req["price"]
            available_quantity = req["available_quantity"]

            response = AssetController.create_new_asset (
                symbol, name, price, available_quantity
            )

            r.status_code = 201
            r.data = json.dumps({
                "title" : "Asset was created successfully.",
                "status" : 201
            })
        except KeyError:
            r.status_code = 400
            r.data = json.dumps({
                "title" : "There were missing arguments for the creation of the asset. You must provide a symbol, a name, a price and the available quantity.",
                "status" : 400
            })
        except exceptions.AssetAlreadyExistsException as e:
            r.status_code = 409
            r.data = json.dumps({
                "title" : str(e),
                "status" : 409,
            })

    return r

        
@app.route("/assetset", methods = ["GET"])
def asset_set():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    try:
        response = AssetController.get_all_assets()
        r.status_code = 200
        r.data = json.dumps(response)
    except exceptions.AssetNotFoundException as e:
        r.status_code = 404
        r.data = json.dumps({
            "title" : str(e),
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

    r.status_code = 200
    r.data = json.dumps({
        "title" : "User logged in",
        "status" : 200
    })

    print("session: ", session['client_id'])
    return r


@app.route("/user", methods = ["GET"])
def user():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    return_not_authenticated_error()

    response = ClientController.get_user_balance_assets(session["client_id"])
    print(response)
    r.status_code = 200
    r.data = json.dumps(response)

    return r


@app.route("/buy", methods = ["POST"])
def buy_asset():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    return_not_authenticated_error()

    symbol = request.get_json()["symbol"]
    quantity = request.get_json()["quantity"]

    try:
        response = ClientController.buy_asset(session['client_id'], symbol, quantity)
        r.status_code = 200
        r.data = json.dumps({
            "title" : "Asset bought succesfully.",
            "status" : 200
        })
    except exceptions.AssetNotFoundException as e:
        r.status_code = 404
        r.data = json.dumps({
            "title" : str(e),
            "status" : 404
        })
    except exceptions.AssetNotEnoughQuantityException as e:
        r.status_code = 409
        r.data = json.dumps({
            "title" : str(e),
            "status" : 409
        })

    return r


@app.route("/sell", methods = ["POST"])
def sell_asset():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    return_not_authenticated_error()

    symbol = request.get_json()["symbol"]
    quantity = request.get_json()["quantity"]

    try:
        response = ClientController.sell_asset(session['client_id'], symbol, quantity)
        r.status_code = 200
        r.data = json.dumps({
            "title" : "Asset sold succesfully.",
            "status" : 200
        })
    except exceptions.AssetNotFoundException as e:
        r.status_code = 404
        r.data = json.dumps({
            "title" : str(e),
            "status" : 404
        })
    except exceptions.ClientNotEnoughAsset as e:
        r.status_code = 409
        r.data = json.dumps({
            "title" : str(e),
            "status" : 409
        })

    return r


@app.route("/deposit", methods = ["POST"])
def deposit():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    return_not_authenticated_error()

    amount = request.get_json()["amount"]

    try:
        response = ClientController.deposit(session['client_id'], amount)
        r.status_code = 200
        r.data = json.dumps({
            "title" : "Amount deposited successfully.",
            "status" : 200
        })
    except Exception as e:
        r.status_code = 409
        r.data = json.dumps({
            "title" : str(e),
            "status" : 409
        })

    return r


@app.route("/withdraw", methods = ["POST"])
def withdraw():
    r = make_response()
    r.headers["Content-type"] = "application/api-problem+json"

    return_not_authenticated_error()

    amount = request.get_json()["amount"]

    try:
        response = ClientController.withdraw(session['client_id'], amount)
        r.status_code = 200
        r.data = json.dumps({
            "title" : "Amount withdrawn successfully.",
            "status" : 200
        })
    except Exception as e:
        r.status_code = 409
        r.data = json.dumps({
            "title" : str(e),
            "status" : 409
        })

    return r


#TODO
# @app.route("/transactions", methods = ["GET"])
# def transactions(id):
#     response = ClientController.transactions()
#     return response
    

if __name__ == "__main__":
    app.run()

