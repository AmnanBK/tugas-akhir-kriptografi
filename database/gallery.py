import os
import sqlite3
from datetime import datetime
from database.db_connection import get_connection

GALLERY_DIR = os.path.join("data", "images")


def add_stego_image(title: str, image_data: bytes, user_id: int) -> bool:
    try:
        os.makedirs(GALLERY_DIR, exist_ok=True)
        file_name = (
            f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        )
        file_path = os.path.join(GALLERY_DIR, file_name)

        with open(file_path, "wb") as f:
            f.write(image_data)

        with get_connection() as conn:
            cursor = conn.cursor()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO gallery (title, stego_path, user_id, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (title, file_path, user_id, created_at),
            )
            conn.commit()
            return True

    except (sqlite3.Error, OSError) as e:
        print("Error (add_stego_image):", e)
        return False


# READ - Ambil semua gambar milik user
def get_all_stego_images(user_id: int) -> list:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, stego_path, created_at
                FROM gallery
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,),
            )
            rows = cursor.fetchall()
            return [
                {"id": r[0], "title": r[1], "file_path": r[2], "created_at": r[3]}
                for r in rows
            ]
    except sqlite3.Error as e:
        print("Database Error (get_all_stego_images):", e)
        return []


# READ - Ambil gambar berdasarkan ID
def get_stego_image_by_id(image_id: int, user_id: int) -> dict | None:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, stego_path, created_at
                FROM gallery
                WHERE id = ? AND user_id = ?
                """,
                (image_id, user_id),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "title": row[1],
                    "file_path": row[2],
                    "created_at": row[3],
                }
            return None
    except sqlite3.Error as e:
        print("Database Error (get_stego_image_by_id):", e)
        return None


# DELETE - Hapus gambar
def delete_stego_image(image_id: int, user_id: int) -> bool:
    try:
        image_info = get_stego_image_by_id(image_id, user_id)
        if not image_info:
            return False

        file_path = image_info["file_path"]

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM gallery WHERE id = ? AND user_id = ?", (image_id, user_id)
            )
            conn.commit()

        if os.path.exists(file_path):
            os.remove(file_path)

        return True

    except (sqlite3.Error, OSError) as e:
        print("Error (delete_stego_image):", e)
        return False
