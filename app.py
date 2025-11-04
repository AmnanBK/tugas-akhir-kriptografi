import os
import time
import streamlit as st
from utils.validators import (
    validate_email,
    validate_password,
    validate_username,
    validate_caesar_key,
    validate_vigenere_key,
)
from utils.ui_components import hide_default_sidebar
from dotenv import load_dotenv
from database.users import login_user, register_user
from database.settings import get_user_settings
from crypto.aes128 import encrypt_aes

load_dotenv()

st.set_page_config(page_title="Private Vault App", page_icon="🔐", layout="centered")


def show_login():
    st.title("🔐 Private Vault App")
    st.subheader("Masuk untuk mengakses brankasmu 🔑")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username.strip() == "" or password.strip() == "":
            st.error("Username dan password wajib diisi!")
        else:
            with st.spinner("Memeriksa akun..."):
                user = login_user(username, password)
            if user:
                st.success("Login berhasil! Mengarahkan ke dashboard...")
                st.session_state["logged_in"] = True
                st.session_state["username"] = user["username"]
                st.session_state["user_id"] = user["id"]

                settings = get_user_settings(user["id"])
                if settings:
                    st.session_state["user_settings"] = settings
                else:
                    st.session_state["user_settings"] = {}

                st.rerun()
            else:
                st.error("Username atau password salah!")

    st.markdown("---")
    st.caption("Belum punya akun?")
    if st.button("👉 Daftar Sekarang"):
        st.session_state["page"] = "register"
        st.rerun()


def show_register():
    st.title("📝 Daftar Akun Baru")
    st.caption("Buat akun untuk menyimpan catatan dan file terenkripsi dengan aman.")
    st.divider()

    username = st.text_input("👤 Username", key="username_input")
    email = st.text_input("📧 E-mail", key="email_input")
    password = st.text_input("🔒 Password", type="password", key="password_input")
    caesar_key = st.text_input("🔑 Caesar Key", type="password", key="caesar_key_input")
    vigenere_key = st.text_input(
        "🔑 Vigenere Key", type="password", key="vigenere_key_input"
    )

    master_key_str = os.getenv("MASTER_KEY")
    master_key = master_key_str.encode("utf-8") if master_key_str else None

    valid = True

    if st.button("🚀 Daftar"):
        if not all([username.strip(), email.strip(), password.strip()]):
            st.warning("⚠️ Semua field wajib diisi!")
            valid = False
        elif not validate_username(username):
            st.warning("⚠️ Username hanya boleh menggunakan huruf dan angka.")
            valid = False
        elif not validate_email(email):
            st.warning("⚠️ Format email tidak valid!")
            valid = False
        elif not validate_password(password):
            st.warning(
                "⚠️ Panjang password minimal 8 karakter dan tidak mengandung karakter spesial"
            )
            valid = False
        elif not validate_caesar_key(caesar_key):
            st.warning("⚠️ Caesaer Key harus berupa angka antara 0 - 25")
            valid = False
        elif not validate_vigenere_key(vigenere_key):
            st.warning("⚠️ Vigenere Key hanya boleh mengandung huruf")
            valid = False
        elif not master_key:
            st.error("❌ MASTER_KEY tidak ditemukan di file .env")
            valid = False

        if valid:
            try:
                email_enc = encrypt_aes(email, master_key)
                success = register_user(
                    username, password, email_enc, caesar_key, vigenere_key
                )

                if success:
                    st.success("✅ Akun berhasil dibuat!")
                    countdown_placeholder = st.empty()
                    for i in range(3, 0, -1):
                        countdown_placeholder.info(
                            f"🔁 Mengarahkan ke halaman login dalam {i} detik..."
                        )
                        time.sleep(1)
                    st.session_state["page"] = "login"
                    st.rerun()
                else:
                    st.error("❌ Username atau email sudah digunakan.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

    st.markdown("---")
    st.caption("Sudah punya akun?")
    if st.button("🔑 Kembali ke Login"):
        st.session_state["page"] = "login"
        st.rerun()


def main():
    hide_default_sidebar()
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    page = st.session_state.get("page", "login")

    if st.session_state.get("logged_in", False):
        st.switch_page("pages/1_Dashboard.py")
    elif page == "login":
        show_login()
    elif page == "register":
        show_register()


if __name__ == "__main__":
    main()
