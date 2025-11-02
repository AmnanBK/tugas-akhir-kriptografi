import json
import sqlite3
from datetime import datetime
from database.db_connection import get_connection
from utils.encryption_utils import super_encrypt, super_decrypt


# CREATE - Tambah Catatan
def add_note(title: str, encrypted_content: str, user_id: int) -> bool:

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            encrypted_content_json = json.dumps(encrypted_content)
            cursor.execute(
                """
                INSERT INTO notes (title, encrypted_content, created_at, user_id)
                VALUES (?, ?, ?, ?)
                """,
                (title, encrypted_content_json, created_at, user_id),
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print("Database Error (add_note):", e)
        return False


# READ - Ambil Semua Catatan
def get_all_notes(user_id: int) -> list:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, encrypted_content, created_at
                FROM notes
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            notes = [
                {
                    "id": r[0],
                    "title": r[1],
                    "encrypted_content": r[2],
                    "created_at": r[3],
                }
                for r in rows
            ]
            return notes
    except sqlite3.Error as e:
        print("Database Error (get_all_notes):", e)
        return []


# READ - Ambil Catatan Berdasarkan ID
def get_note_by_id(note_id: int, user_id: int) -> dict | None:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, encrypted_content, created_at
                FROM notes
                WHERE id = ? AND user_id = ?
                """,
                (note_id, user_id),
            )
            row = cursor.fetchone()
            if row:

                return {
                    "id": row[0],
                    "title": row[1],
                    "content": json.loads(row[2]),
                    "created_at": row[3],
                }
            return None
    except sqlite3.Error as e:
        print("Database Error (get_note_by_id):", e)
        return None


# UPDATE - Perbarui Catatan
def update_note(note_id: int, title: str, encrypted_content, user_id: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            encrypted_content_json = json.dumps(encrypted_content)
            cursor.execute(
                """
                UPDATE notes
                SET title = ?, encrypted_content = ?
                WHERE id = ? AND user_id = ?
                """,
                (title, encrypted_content_json, note_id, user_id),
            )
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print("Database Error (update_note):", e)
        return False


# DELETE - Hapus Catatan
def delete_note(note_id: int, user_id: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print("Database Error (delete_note):", e)
        return False
