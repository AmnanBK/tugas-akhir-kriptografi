import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database.settings import update_user_settings
from database.users import update_user_password, get_user_by_id, get_password_by_id, delete_user
from crypto.hash_sha256 import hash_password
from database.settings import get_user_settings

user_id = st.session_state.get("user_id")

user = get_user_by_id(user_id)
user_settings = get_user_settings(user_id)

FILE_DIR = "data/files"
os.makedirs(FILE_DIR, exist_ok=True)

# RC4 Dummy
def rc4_encrypt_decrypt(key, data):
    # untuk contoh, kita return data apa adanya
    return data

def main():
    st.set_page_config(page_title="Pengaturan", layout="wide")

    # Simulasi login sementara
    username = st.session_state.get("username", "UserDemo")

    # Sidebar
    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")

        st.divider()
        # Tombol navigasi
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("📝 Tambah Catatan", use_container_width=True):
            st.switch_page("pages/2_Add_Note.py")
        if st.button("🔒 Brankas Pribadi", use_container_width=True):
            st.switch_page("pages/4_File_Vault.py")
        if st.button("🖼️ Galeri Rahasia", use_container_width=True):
            st.switch_page("pages/5_Gallery.py")
        if st.button("⚙️ Pengaturan", use_container_width=True):
            st.switch_page("pages/6_Settings.py")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")

    # Pengaturan
    st.title("⚙️ Pengaturan")
    st.divider()
    caesar_key = user_settings["caesar_key"] if user_settings and user_settings["caesar_key"] else "-"
    vigenere_key = user_settings["vigenere_key"] if user_settings and user_settings["vigenere_key"] else "-"
    vault_key = user_settings["vault_key"] if user_settings and user_settings["vault_key"] else "-"

    st.subheader("Pengaturan Key")
    caesar_key = st.text_input("Masukkan Caesar Key", value=caesar_key, type="password")
    vigenere_key = st.text_input("Masukkan Vigenere Key", value=vigenere_key, type="password")
    vault_key = st.text_input("Vault Key", value=vault_key, type="password")
    # master_key = st.text_input("Masukkan Master Key", type="password")

    if st.button("Simpan Key"):
        if caesar_key and vigenere_key and vault_key:
            # enkripsi key di sini jika perlu
            # update_master_key(username, master_key)
            update_user_settings(user_id=user_id,
                        caesar_key=caesar_key,
                        vigenere_key=vigenere_key,
                        vault_key=vault_key)
            st.success("Semua key berhasil disimpan!")
        else:
            st.warning("Master Key tidak boleh kosong.")

    st.divider()

    # Ganti password
    st.subheader("Ganti Password")
    old_pass = st.text_input("Password Lama", type="password")
    new_pass = st.text_input("Password Baru", type="password")
    old_hashed = hash_password(old_pass)
    if st.button("Simpan"):
        if old_pass and new_pass:
            stored_hash = get_password_by_id(user_id)
            if stored_hash is None:
                st.error("User tidak ditemukan")
            elif (old_hashed != stored_hash):
                st.error("Password lama salah.")
            else:
                new_hashed = hash_password(new_pass)
                success = update_user_password(user_id, new_hashed)
                if success:
                    st.success("Password berhasil diperbarui!")
                else:
                    st.warning("Gagal memperbarui password!")
        else:
            st.warning("Password tidak boleh kosong!")

    st.divider()

    # Hapus akun
    st.subheader("Hapus Akun")
    st.warning("⚠️ Akun akan dihapus secara permanen")

    confirm = st.checkbox("Saya yakin ingin menghapus akun ini")

    if confirm:
        if st.button("Hapus Akun"):
            deleted = delete_user(user_id)
            if deleted:
                st.success("Akun berhasil dihapus!")
                st.session_state.clear()
                st.switch_page("app.py") 
            else:
                st.error("Gagal menghapus akun")

if __name__ == "__main__":
    main()
