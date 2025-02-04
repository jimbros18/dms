import pandas as pd
import sqlite3

def get_data():
    connection = sqlite3.connect("./DB/clientDB.sqlite3")
    df = pd.read_sql_query("SELECT * FROM client;", connection)
    return df

# print(get_data())