import sqlite3
from database.db_connection import get_connection


# CREATE - Register User
def register_user(username: str, password: str, email: str) -> bool:
    password_hash = password  # akan diganti dengan hash

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email),
            )
            existing = cursor.fetchone()
            if existing:
                return False

            cursor.execute(
                """
                INSERT INTO users (username, password_hash, email)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, email),
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print("Database Error (register_user):", e)
        return False


# READ - Login User
def login_user(username: str, password: str) -> dict | None:
    password_hash = password  # akan diganti dengan hash

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash),
            )
            user = cursor.fetchone()
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            else:
                return None
    except sqlite3.Error as e:
        print("Database Error (login_user):", e)
        return None


# READ - Get User by ID
def get_user_by_id(user_id: int) -> dict | None:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
            )
            user = cursor.fetchone()
            if user:
                return {"id": user[0], "username": user[1], "email": user[2]}
            return None
    except sqlite3.Error as e:
        print("Database Error (get_user_by_id):", e)
        return None


# DELETE - Delete User
def delete_user(user_id: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print("Database Error (delete_user):", e)
        return False
