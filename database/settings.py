import sqlite3
from database.db_connection import get_connection


# CREATE - Tambah / Inisialisasi Pengaturan Default untuk User Baru
def create_user_settings(user_id: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO settings (user_id, caesar_key, vigenere_key, rsa_private, rsa_public, vault_key)
                VALUES (?, NULL, NULL, NULL, NULL, NULL)
                """,
                (user_id,),
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print("Database Error (create_user_settings):", e)
        return False


# READ - Ambil Semua Pengaturan User
def get_user_settings(user_id: int) -> dict | None:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, caesar_key, vigenere_key, rsa_private, rsa_public, vault_key
                FROM settings
                WHERE user_id = ?
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "caesar_key": row[1],
                    "vigenere_key": row[2],
                    "rsa_private": row[3],
                    "rsa_public": row[4],
                    "vault_key": row[5],
                }
            return None
    except sqlite3.Error as e:
        print("Database Error (get_user_settings):", e)
        return None


# UPDATE - Perbarui Kunci / Pengaturan User
def update_user_settings(
    user_id: int,
    caesar_key: str | None = None,
    vigenere_key: str | None = None,
    rsa_private: str | None = None,
    rsa_public: str | None = None,
    vault_key: str | None = None,
) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            fields = []
            values = []

            if caesar_key is not None:
                fields.append("caesar_key = ?")
                values.append(caesar_key)
            if vigenere_key is not None:
                fields.append("vigenere_key = ?")
                values.append(vigenere_key)
            if rsa_private is not None:
                fields.append("rsa_private = ?")
                values.append(rsa_private)
            if rsa_public is not None:
                fields.append("rsa_public = ?")
                values.append(rsa_public)
            if vault_key is not None:
                fields.append("vault_key = ?")
                values.append(vault_key)

            if not fields:
                return False

            values.append(user_id)

            query = f"UPDATE settings SET {', '.join(fields)} WHERE user_id = ?"
            cursor.execute(query, tuple(values))
            conn.commit()
            return cursor.rowcount > 0

    except sqlite3.Error as e:
        print("Database Error (update_user_settings):", e)
        return False


# DELETE - Hapus Pengaturan User
def delete_user_settings(user_id: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM settings WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print("Database Error (delete_user_settings):", e)
        return False
