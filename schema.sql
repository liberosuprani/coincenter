PRAGMA foreign_keys = ON;

CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY,
    is_manager BOOLEAN NOT NULL,
    balance FLOAT
);

CREATE TABLE Assets (
    asset_symbol VARCHAR(5) PRIMARY KEY,
    asset_name VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    available_quantity INTEGER NOT NULL
);

CREATE TABLE ClientAssets (
    client_id INTEGER NOT NULL,
    asset_symbol VARCHAR(5) NOT NULL,
    quantity FLOAT NOT NULL,

    FOREIGN KEY (client_id)
    REFERENCES Clients(client_id)
    ON DELETE CASCADE,

    FOREIGN KEY (asset_symbol)
    REFERENCES Assets(asset_symbol)
    ON DELETE CASCADE
);

CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    asset_symbol VARCHAR(5) NOT NULL,
    [type] VARCHAR NOT NULL,
    quantity FLOAT NOT NULL,
    price FLOAT NOT NULL,
    [time] DATE NOT NULL,

    FOREIGN KEY (client_id)
    REFERENCES Clients(client_id),

    FOREIGN KEY (asset_symbol)
    REFERENCES Assets(asset_symbol)
);