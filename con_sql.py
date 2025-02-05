import pandas as pd
import sqlite3

def get_db():
    connection = sqlite3.connect("./DB/clientDB.sqlite3")
    df = pd.read_sql_query("SELECT * FROM client;", connection)
    return df

def get_client_id(row_id):
    connection = sqlite3.connect("./DB/clientDB.sqlite3")
    query = "SELECT * FROM client WHERE id = ?;"
    df = pd.read_sql_query(query, connection, params=(row_id,))
    return df.iloc[0].to_dict()