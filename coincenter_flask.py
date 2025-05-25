"""
Aplicações Distribuídas - Projeto 3 - coincenter_flask.py
Número de aluno: 62220
"""

#TODO get_assets_balance do user não deveria mostrar a available_quantity de cada asset que ele tem

from flask import Flask, request, make_response, session
import json, ssl
from coincenter_data import *
from kazoo.client import KazooClient

app = Flask(__name__)
app.secret_key = "chave secreta"

def return_not_authenticated_error():
    r = make_response()
    r.headers["Content-type"] = "application/json"

    if "client_id" not in session:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = 401
        r.data = json.dumps({
            "title" : "Not logged in.",
            "detail" : "You must be logged in for this operation to work.",
            "status" : 401
        })
        return r
    
    return False

@app.route("/asset", methods = ["POST"])
@app.route("/asset/<string:symbol>", methods = ["GET"])
def asset(symbol=None):
    r = make_response()
    r.headers["Content-type"] = "application/json"

    if request.method == "GET":
        try:
            response = AssetController.get_asset(symbol)
            r.status_code = 200
            r.data = json.dumps(response)
        except NotFoundException as e:
            r.headers["Content-type"] = "application/api-problem+json"
            r.status_code = 404
            r.data = json.dumps({
                "title" : e.title,
                "status" : 404,
                "detail" : str(e)
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
            zk.create(f"/asset/{symbol}-", ephemeral=False, sequence=True)

        except KeyError:
            r.headers["Content-type"] = "application/api-problem+json"
            r.status_code = 400
            r.data = json.dumps({
                "title" : "There were missing arguments for the creation of the asset.",
                "detail" : "You must provide a symbol, a name, a price and the available quantity.",
                "status" : 400
            })
        except Exception as e:
            r.headers["Content-type"] = "application/api-problem+json"
            r.status_code = e.code
            r.data = json.dumps({
                "title" : e.title,
                "status" : e.code,
                "detail" : e.detail
            })

    return r

        
@app.route("/assetset/<symbols>", methods = ["GET"])
@app.route("/assetset", methods = ["GET"])
def asset_set(symbols=""):
    r = make_response()
    r.headers["Content-type"] = "application/json"


    try:
        if len(symbols) == 0:
            response = AssetController.get_all_assets()
        else:
            symbols_list = symbols.split()
            response = AssetController.get_asset_set(symbols_list)
        r.status_code = 200
        r.data = json.dumps(response)
    except NotFoundException as e:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = e.code
        r.data = json.dumps({
            "title" : e.title,
            "status" : e.code,
            "detail" : e.detail
        })
    return r


@app.route("/login", methods = ["POST"])
def login():
    r = make_response()
    r.headers["Content-type"] = "application/json"

    req = request.get_json()
    client_id = req["client_id"]

    response = ClientController.login(client_id)

    r.status_code = 200
    r.data = json.dumps({
        "title" : "User logged in",
        "status" : 200
    })

    return r


@app.route("/user", methods = ["GET"])
def user():
    r = make_response()
    r.headers["Content-type"] = "application/json"

    return_not_authenticated_error()

    response = ClientController.get_user_balance_assets(session["client_id"])
    r.status_code = 200
    r.data = json.dumps(response)

    return r


@app.route("/buy", methods = ["POST"])
def buy_asset():
    r = make_response()
    r.headers["Content-type"] = "application/json"

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
    except KeyError:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = 400
        r.data = json.dumps({
            "title" : "There were missing arguments.",
            "detail" : "You must provide a symbol and a quantity.",
            "status" : 400
        })
    except Exception as e:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = e.code
        r.data = json.dumps({
            "title" : e.title,
            "detail" : e.detail,
            "status" : e.code
        })

    return r


@app.route("/sell", methods = ["POST"])
def sell_asset():
    r = make_response()
    r.headers["Content-type"] = "application/json"

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
    except KeyError:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = 400
        r.data = json.dumps({
            "title" : "There were missing arguments for the creation of the asset.",
            "detail" : "You must provide a symbol, a name, a price and the available quantity.",
            "status" : 400
        })
    except Exception as e:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = e.code
        r.data = json.dumps({
            "title" : e.title,
            "detail" : e.detail,
            "status" : e.code
        })

    return r


@app.route("/deposit", methods = ["POST"])
def deposit():
    r = make_response()
    r.headers["Content-type"] = "application/json"

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
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = e.code
        r.data = json.dumps({
            "title" : e.title,
            "detail" : e.detail,
            "status" : e.code
        })

    return r


@app.route("/withdraw", methods = ["POST"])
def withdraw():
    r = make_response()
    r.headers["Content-type"] = "application/json"

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
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = e.code
        r.data = json.dumps({
            "title" : e.title,
            "detail" : e.detail,
            "status" : e.code
        })

    return r


@app.route("/transactions", methods = ["GET"])
def transactions():
    r = make_response()
    r.headers["Content-type"] = "application/json"

    try:
        response = ClientController.get_transactions(session["client_id"])
        r.status_code = 200
        r.data = json.dumps(response)
    except Exception as e:
        r.headers["Content-type"] = "application/api-problem+json"
        r.status_code = e.code
        r.data = json.dumps({
            "title" : e.title,
            "detail" : e.detail,
            "status" : e.code
        })

    return r
    

if __name__ == "__main__":
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile="root.pem")
    context.load_cert_chain(certfile="serv.crt", keyfile="serv.key")

    zk = KazooClient(hosts="127.0.0.1:2181")
    zk.start()
    zk.ensure_path("/asset")

    app.run("localhost" , ssl_context=context, debug=True)