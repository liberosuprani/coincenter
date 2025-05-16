import requests

def main():
    # print("-- Teste create_asset --")
    # symbol = input("Símbolo: ")
    # name = input("Nome: ")
    # price = float(input("Preço: "))
    # available_quantity = int(input("Quantidade disponível: "))

    # asset = {
    #     "symbol" : symbol,
    #     "name" : name,
    #     "price" : price,
    #     "available_quantity" : available_quantity
    # }

    # r = requests.post("http://localhost:5000/asset", json = asset)

    ######################################################################

    # print("-- Teste get_asset")
    # asset_symbol = "BTC"
    # r = requests.get(f"http://localhost:5000/asset/{asset_symbol}")

    ######################################################################

    # print("-- Teste get_all_assets --")
    # r = requests.get("http://localhost:5000/assetset")

    ######################################################################

    # client_id = 10
    # a = {
    #     "client_id" : client_id
    # }
    # r = requests.post("http://localhost:5000/login", json = a) 

    ######################################################################

    # print("-- Teste get_user_balance_assets --")
    # client_id = 666
    # r = requests.get(f"http://localhost:5000/user/{client_id}")

    ######################################################################

    # print("-- Teste buy_asset --")
    # a = {
    #     "symbol": "BTC",
    #     "quantity" : 1 
    # }
    # r = requests.post("http://localhost:5000/buy", json=a)

    ######################################################################
    
    # print("-- Teste sell_asset --")
    # a = {
    #     "symbol": "BTC",
    #     "quantity" : 1 
    # }
    # r = requests.post("http://localhost:5000/sell", json=a)
    
    ######################################################################

    # print("-- Teste deposit --")
    # deposit = {
    #     "amount" : 100
    # }
    # r = requests.post("http://localhost:5000/deposit", json = deposit)
    
    ######################################################################

    # print("-- Teste withdraw --")
    # withdraw = {
    #     "amount" : 99
    # }
    # r = requests.post("http://localhost:5000/withdraw", json = withdraw)
    
    ######################################################################
    
    print(r.text)

if __name__ == "__main__":
    main()