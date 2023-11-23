import sqlite3
import string
import random

connection = sqlite3.connect("api_keys.sql")
cursor = connection.cursor()

characters = string.ascii_letters + string.digits
api_key = ''.join(random.choice(characters) for i in range(30))
print(api_key)

cursor.execute("INSERT INTO API_KEYS (api_key) VALUES (?)", (api_key,))
connection.commit()
connection.close()