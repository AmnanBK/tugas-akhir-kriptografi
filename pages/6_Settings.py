import streamlit as st
import os
from database.settings import update_user_settings
from database.users import (
    update_user_password,
    get_password_by_id,
    delete_user,
)
from crypto.hash_sha256 import hash_password
from database.settings import get_user_settings
from utils.auth_utils import check_login
from utils.ui_components import show_sidebar


FILE_DIR = "data/files"
os.makedirs(FILE_DIR, exist_ok=True)

st.set_page_config(page_title="Pengaturan", layout="wide")


def section_manage_keys(user_id):
    st.subheader("🔐 Pengaturan Key")
    st.info("Atur kunci enkripsi yang digunakan untuk operasi keamanan.")

    user_settings = get_user_settings(user_id)

    caesar_key = (
        user_settings["caesar_key"]
        if user_settings and user_settings["caesar_key"]
        else ""
    )
    vigenere_key = (
        user_settings["vigenere_key"]
        if user_settings and user_settings["vigenere_key"]
        else ""
    )
    vault_key = (
        user_settings["vault_key"]
        if user_settings and user_settings["vault_key"]
        else ""
    )

    caesar_key = st.text_input("Masukkan Caesar Key", value=caesar_key, type="password")
    vigenere_key = st.text_input(
        "Masukkan Vigenere Key", value=vigenere_key, type="password"
    )
    vault_key = st.text_input("Vault Key", value=vault_key, type="password")

    if st.button("💾 Simpan Key"):
        if caesar_key and vigenere_key and vault_key:
            update_user_settings(
                user_id=user_id,
                caesar_key=caesar_key,
                vigenere_key=vigenere_key,
                vault_key=vault_key,
            )
            st.success("✅ Semua key berhasil disimpan!")
        else:
            st.warning("⚠️ Semua key harus diisi!")


def section_change_password(user_id):
    st.subheader("🔒 Ganti Password")
    st.info("Ubah password akun Anda dengan memasukkan password lama dan baru.")

    old_pass = st.text_input("Password Lama", type="password")
    new_pass = st.text_input("Password Baru", type="password")

    if st.button("🔁 Simpan Password Baru"):
        if old_pass and new_pass:
            stored_hash = get_password_by_id(user_id)
            if stored_hash is None:
                st.error("❌ User tidak ditemukan.")
                return

            if hash_password(old_pass) != stored_hash:
                st.error("❌ Password lama salah.")
                return

            new_hashed = hash_password(new_pass)
            success = update_user_password(user_id, new_hashed)
            if success:
                st.success("✅ Password berhasil diperbarui!")
            else:
                st.error("⚠️ Gagal memperbarui password!")
        else:
            st.warning("⚠️ Password lama dan baru tidak boleh kosong.")


def section_delete_account(user_id):
    st.subheader("🗑️ Hapus Akun")
    st.warning(
        "⚠️ Akun akan dihapus secara permanen. Tindakan ini tidak dapat dibatalkan."
    )

    confirm = st.checkbox("Saya yakin ingin menghapus akun ini")

    if confirm:
        if st.button("❌ Hapus Akun Sekarang"):
            deleted = delete_user(user_id)
            if deleted:
                st.success("✅ Akun berhasil dihapus!")
                st.session_state.clear()
                st.switch_page("app.py")
            else:
                st.error("❌ Gagal menghapus akun.")


def show_setting():
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("⚠️ Anda belum login.")
        st.stop()

    st.title("⚙️ Pengaturan Akun")
    st.divider()

    tab1, tab2, tab3 = st.tabs(
        ["🔑 Pengaturan Key", "🔒 Ganti Password", "🗑️ Hapus Akun"]
    )

    with tab1:
        section_manage_keys(user_id)

    with tab2:
        section_change_password(user_id)

    with tab3:
        section_delete_account(user_id)


def main():
    check_login()
    show_sidebar()
    show_setting()


if __name__ == "__main__":
    main()
