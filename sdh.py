import os

# Hardcoded secret - security issue for agent to find
API_KEY = "sk-1234567890abcdef"

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query
