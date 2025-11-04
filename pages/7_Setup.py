import streamlit as st
import os
from database.settings import update_user_settings
from database.settings import get_user_settings
from utils.auth_utils import check_login

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

    caesar_key = st.text_input("Masukkan Caesar Key", value=caesar_key, type="password")
    vigenere_key = st.text_input(
        "Masukkan Vigenere Key", value=vigenere_key, type="password"
    )

    if st.button("💾 Simpan Key"):
        if caesar_key and vigenere_key:
            update_user_settings(
                user_id=user_id,
                caesar_key=caesar_key,
                vigenere_key=vigenere_key,
            )
            st.success("✅ Semua key berhasil disimpan!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.warning("⚠️ Semua key harus diisi!")


def main():
    section_manage_keys(st.session_state.get("user_id"))


if __name__ == "__main__":
    main()
