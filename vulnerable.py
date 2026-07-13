import os
import sqlite3
import hashlib

SECRET_KEY = "hardcoded-secret-key-12345"
DB_PASSWORD = "admin123"
API_TOKEN = "sk-prod-abc123def456"

def login(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_data(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    data = cursor.fetchall()
    conn.close()
    return data

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def authenticate(token):
    if token == API_TOKEN:
        return True
    return False

# TODO: fix security issues
