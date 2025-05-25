"""
Aplicações Distribuídas - Projeto 3 - setup_db.py
Número de aluno: 62220
"""

import sqlite3
from os.path import isfile
from flask import g

def get_db(db_name = "coincenter.db"):
    is_db_created = isfile(db_name)

    db_connection = sqlite3.connect(db_name)
    cursor = db_connection.cursor()

    if not is_db_created:
        with open("schema.sql", "r") as f:
            schema = f.read()
            cursor.executescript(schema)

    if "db" not in g:
        g.db = db_connection
        g.db.row_factory = sqlite3.Row

    return g.db

if __name__ ==  "__main__":
    is_db_created = isfile("coincenter.db")

    db_connection = sqlite3.connect("coincenter.db")
    cursor = db_connection.cursor()

    if not is_db_created: 
        with open("schema.sql", "r") as f:
            schema = f.read()
            cursor.executescript(schema)

    query = "INSERT INTO Assets(asset_symbol, asset_name, price, available_quantity)" \
        " VALUES (?, ?, ?, ?);"

    cursor.execute(query, ("BTC", "BITCOIN", 1000, 10))