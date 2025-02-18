import pandas as pd
import sqlite3

def get_db():
    connection = sqlite3.connect("./DB/clientDB.sqlite3")
    df = pd.read_sql_query("SELECT * FROM client;", connection)
    return df

def get_keys():
    connection = sqlite3.connect("./DB/clientDB.sqlite3")
    try:
        df = pd.read_sql_query("SELECT * FROM client LIMIT 1;", connection)
        return df.keys() 
    finally:
        connection.close()

def get_client_id(row_id):
    connection = sqlite3.connect("./DB/clientDB.sqlite3")
    query = "SELECT * FROM client WHERE id = ?;"
    df = pd.read_sql_query(query, connection, params=(row_id,))
    return df.iloc[0].to_dict()

def update_info(newdata):
    if 'id' not in newdata:
        print("Error: 'id' key is required to update the record.")
        return False
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("./DB/clientDB.sqlite3")
        cursor = conn.cursor()

        # Update query
        update_query = """
            UPDATE client SET
                first_name = ?, middle_name = ?, last_name = ?, nickname = ?, birthdate = ?, 
                deathdate = ?, address = ?, age = ?, religion = ?, coffin = ?, amount = ?, 
                gov_ass = ?, mor_plan = ?, mor_plan_amount = ?, accessories = ?
            WHERE id = ?
        """
        cursor.execute(update_query, (
            newdata['first_name'], newdata['middle_name'], newdata['last_name'], newdata['nickname'], 
            newdata['birthdate'], newdata['deathdate'], newdata['address'], newdata['age'], 
            newdata['religion'], newdata['coffin'], newdata['amount'], newdata['gov_ass'], 
            newdata['mor_plan'], newdata['mor_plan_amount'], newdata['accessories'], newdata['id']
        ))
        conn.commit()

        # Verify update
        updated_df = pd.read_sql(f"SELECT * FROM client WHERE id = {newdata['id']}", conn)
        # print("Updated Record:\n", updated_df)
        updated_df


        conn.close()
        return True

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False
    
def save_to_db(n_data):
    """Saves entry values to SQLite database."""
    conn = sqlite3.connect("./DB/clientDB.sqlite3")
    cursor = conn.cursor()

    # Insert only the columns excluding 'id' (since it's auto-incremented)
    cursor.execute("""
        INSERT INTO client (first_name, middle_name, last_name, nickname, birthdate, deathdate, 
                            address, age, religion, coffin, amount, gov_ass, mor_plan, 
                            mor_plan_amount, accessories) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", n_data)

    conn.commit()
    conn.close()
    print("Data saved successfully!")