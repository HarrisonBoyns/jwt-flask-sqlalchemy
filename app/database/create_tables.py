import sqlite3

# Auto-incrementing id
create_user_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
create_item_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, item text, price real)"
insert_data = "INSERT INTO items VALUES (Null, 'cheese', 18.99, 1)"

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

cursor.execute(create_user_table)
cursor.execute(create_item_table)
cursor.execute(insert_data)

connection.commit()

connection.close()