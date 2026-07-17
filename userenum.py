import sqlite3

username = input("Username: ")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Vulnerable
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
