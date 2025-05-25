"""
Aplicações Distribuídas - Projeto 3 - setup_db.py
Número de aluno: 62220
"""

import sqlite3
from os.path import isfile
from flask import g

def get_db(db_name = "coincenter.db"):
    # checks if there is a .db file in this directory
    is_db_created = isfile(db_name)

    # connects to the database with the given name
    # if the database does not exist, it is created
    db_connection = sqlite3.connect(db_name)
    cursor = db_connection.cursor()

    # if db did not exist prior to this method, it executes the script
    # to create the tables
    if not is_db_created:
        with open("schema.sql", "r") as f:
            schema = f.read()
            cursor.executescript(schema)

    # if the key 'db' does not exist in flask's g variable
    # it is created 
    if "db" not in g:
        g.db = db_connection
        g.db.row_factory = sqlite3.Row

    return g.db

# testing purposes
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