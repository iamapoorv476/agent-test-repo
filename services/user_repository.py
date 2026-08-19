"""
Data access layer for user records.
"""
import sqlite3

DB_PATH = "app.db"


def get_user_by_id(user_id: str) -> dict | None:
    """Fetches a single user by their internal id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, email, stripe_customer_id, created_at FROM users WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "stripe_customer_id": row[2],
        "created_at": row[3],
    }


def get_users_with_recent_orders(order_ids: list[str]) -> list[dict]:
    """Fetches user details for a batch of order ids."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    results = []
    for order_id in order_ids:
        cursor.execute(
            "SELECT user_id FROM orders WHERE id = ?", (order_id,)
        )
        row = cursor.fetchone()
        if row is None:
            continue
        user = get_user_by_id(row[0])
        if user:
            results.append(user)

    conn.close()
    return results


def update_user_email(user_id: str, new_email: str) -> bool:
    """Updates a user's email address."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def deactivate_user(user_id: str):
    """Marks a user account as inactive."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET is_active = 0 WHERE id = ?",
            (user_id,),
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()
