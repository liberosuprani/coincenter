PRAGMA foreign_keys = ON;

CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY,
    is_manager BOOLEAN,
    balance FLOAT
);

CREATE TABLE Assets (
    asset_symbol VARCHAR(5) PRIMARY KEY,
    asset_name VARCHAR,
    price FLOAT,
    available_quantity INTEGER
);

CREATE TABLE ClientAssets (
    client_id INTEGER,
    asset_symbol VARCHAR(5),
    quantity FLOAT,

    FOREIGN KEY (client_id)
    REFERENCES Clients(client_id)
    ON DELETE CASCADE,

    FOREIGN KEY (asset_symbol)
    REFERENCES Assets(asset_symbol)
    ON DELETE CASCADE
);

CREATE TABLE Transactions (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    client_id INTEGER,
    asset_symbol VARCHAR(5),
    [type] VARCHAR,
    quantity FLOAT,
    price FLOAT,
    [time] DATE,

    FOREIGN KEY (client_id)
    REFERENCES Clients(client_id),

    FOREIGN KEY (asset_symbol)
    REFERENCES Assets(asset_symbol)
);