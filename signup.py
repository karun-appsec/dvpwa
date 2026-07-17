import os
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

# -----------------------
# SQL Injection
# -----------------------
@app.route("/signup")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Vulnerable
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    return str(result)


# -----------------------
# Command Injection
# -----------------------
@app.route("/ping")
def ping():
    host = request.args.get("host")

    # Vulnerable
    output = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True
    )

    return output.decode()


# -----------------------
# Path Traversal
# -----------------------
@app.route("/file")
def read_file():
    filename = request.args.get("name")

    # Vulnerable
    with open("uploads/" + filename, "r") as f:
        return f.read()


# -----------------------
# Hardcoded Secret
# -----------------------
AWS_SECRET_KEY = "AKIAEXAMPLESECRETKEY123456"


# -----------------------
# Weak Random
# -----------------------
import random

def generate_token():
    return str(random.randint(100000, 999999))


# -----------------------
# Unsafe Deserialization
# -----------------------
import pickle

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data

    # Vulnerable
    obj = pickle.loads(data)

    return str(obj)


# -----------------------
# Arbitrary Code Execution
# -----------------------
@app.route("/eval")
def run():
    expression = request.args.get("expr")

    # Vulnerable
    return str(eval(expression))


# -----------------------
# Debug Mode Enabled
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
