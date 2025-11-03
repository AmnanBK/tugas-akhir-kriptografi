import os
import sqlite3
from datetime import datetime
from database.db_connection import get_connection

FILES_DIR = os.path.join("data", "files")


# CREATE - Upload File
def add_file(file_name: str, file_data: bytes, user_id: int) -> bool:
    try:
        os.makedirs(FILES_DIR, exist_ok=True)
        file_path = os.path.join(FILES_DIR, file_name)

        with open(file_path, "wb") as f:
            f.write(file_data)

        with get_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO vault (file_name, file_path, user_id, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (file_name, file_path, user_id, created_at),
            )
            conn.commit()
            return True

    except (sqlite3.Error, OSError) as e:
        print("Error (add_file):", e)
        return False


# READ - Ambil Semua File
def get_all_files(user_id: int) -> list:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, file_path, created_at
                FROM vault
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            files = [
                {"id": r[0], "file_name": r[1], "file_path": r[2], "created_at": r[3]}
                for r in rows
            ]
            return files
    except sqlite3.Error as e:
        print("Database Error (get_all_files):", e)
        return []


# READ - Ambil File Berdasarkan ID
def get_file_by_id(file_id: int, user_id: int) -> dict | None:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, file_path, created_at
                FROM vault
                WHERE id = ? AND user_id = ?
                """,
                (file_id, user_id),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "file_name": row[1],
                    "file_path": row[2],
                    "created_at": row[3],
                }
            return None
    except sqlite3.Error as e:
        print("Database Error (get_file_by_id):", e)
        return None


# DELETE - Hapus File
def delete_file(file_id: int, user_id: int) -> bool:
    try:
        file_info = get_file_by_id(file_id, user_id)
        if not file_info:
            return False

        file_path = file_info["file_path"]

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM vault WHERE id = ? AND user_id = ?", (file_id, user_id)
            )
            conn.commit()

        if os.path.exists(file_path):
            os.remove(file_path)

        return True

    except (sqlite3.Error, OSError) as e:
        print("Error (delete_file):", e)
        return False
