import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join("data", "secret_diary.db")

os.makedirs("data", exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def test_connection():
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(" Database connected successfully.")
            print(" Existing tables:", [t[0] for t in tables])
    except Exception as e:
        print("Database connection failed:", e)


if __name__ == "__main__":
    test_connection()
