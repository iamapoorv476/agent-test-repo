import sqlite3
import hashlib
import os

# BUG 1: Hardcoded secret (should be CRITICAL)
JWT_SECRET = "super-secret-jwt-key-2024"

# BUG 2: Hardcoded admin password (should be CRITICAL)  
ADMIN_PASSWORD = "admin123"

def login(username: str, password: str):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # BUG 3: SQL injection (should be CRITICAL)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    return cursor.fetchone()

def hash_password(password: str) -> str:
    # BUG 4: MD5 for passwords (should be HIGH)
    return hashlib.md5(password.encode()).hexdigest()

def get_user(user_id: str):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # BUG 5: SQL injection again (should be CRITICAL)
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchall()

def verify_token(token: str) -> bool:
    # BUG 6: Timing attack on string comparison (should be HIGH)
    return token == JWT_SECRET
