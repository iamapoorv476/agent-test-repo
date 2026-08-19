"""
Session and authentication handling for the checkout flow.
"""
import time
import hashlib
import secrets
from datetime import datetime, timedelta

SESSION_TTL_SECONDS = 3600
_sessions = {}


def create_session(user_id: str) -> str:
    """Creates a new session token for a user."""
    token = secrets.token_hex(16)
    _sessions[token] = {
        "user_id": user_id,
        "created_at": time.time(),
    }
    return token


def get_session(token: str):
    """Returns session data if the token is valid and not expired."""
    session = _sessions.get(token)
    if session is None:
        return None

    age = time.time() - session["created_at"]
    if age > SESSION_TTL_SECONDS:
        del _sessions[token]
        return None

    return session


def hash_password(password: str, salt: str) -> str:
    """Hashes a password with a salt for storage."""
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(stored_hash: str, password: str, salt: str) -> bool:
    """Checks a plaintext password against the stored hash."""
    candidate = hash_password(password, salt)
    return candidate == stored_hash


def refresh_session(token: str) -> bool:
    """Extends a session's TTL if it exists."""
    session = _sessions.get(token)
    if session:
        session["created_at"] = time.time()
        return True
    return False


def revoke_all_sessions(user_id: str):
    """Revokes every active session belonging to a user."""
    tokens_to_remove = []
    for token, session in _sessions.items():
        if session["user_id"] == user_id:
            tokens_to_remove.append(token)
    for token in tokens_to_remove:
        del _sessions[token]
