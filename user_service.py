import sqlite3
from typing import List

def get_all_users_with_orders():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users")
    users = cursor.fetchall()
    
    result = []
    for user in users:
        # BUG 1: N+1 query — one query per user (should be MEDIUM/HIGH)
        cursor.execute(f"SELECT * FROM orders WHERE user_id = {user[0]}")
        orders = cursor.fetchall()
        result.append({"user": user, "orders": orders})
    
    # BUG 2: Connection never closed — resource leak (should be MEDIUM)
    return result

def count_active_users():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    # BUG 3: Loading all rows to count instead of COUNT(*) (should be MEDIUM)
    cursor.execute("SELECT * FROM users WHERE active = 1")
    all_users = cursor.fetchall()
    return len(all_users)

def search_users(query: str) -> List[dict]:
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    
    # BUG 4: Loading entire table then filtering in Python (should be MEDIUM)
    return [u for u in all_users if query.lower() in str(u).lower()]
