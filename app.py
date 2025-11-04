import os
import streamlit as st
from utils.validators import validate_email, validate_password, validate_username
from utils.ui_components import hide_default_sidebar
from dotenv import load_dotenv
from database.users import login_user, register_user
from database.settings import get_user_settings
from crypto.aes128 import encrypt_aes

load_dotenv()

st.set_page_config(page_title="Secret Diary App", page_icon="🔐", layout="centered")


def show_login():
    st.title("🔐 Secret Diary App")
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
    st.subheader("Buat akun untuk menyimpan catatan dan file terenkripsi")

    username = st.text_input("Username")
    email = st.text_input("E-mail")
    password = st.text_input("Password", type="password")
    caesar_key = st.text_input("Masukkan Caesar Key", type="password")
    vigenere_key = st.text_input("Masukkan Vigenere Key", type="password")
    master_key_str = os.getenv("MASTER_KEY")
    master_key = master_key_str.encode("utf-8")

    if st.button("Daftar"):
        if username.strip() == "" or password.strip() == "" or email.strip() == "":
            st.error("Semua field wajib diisi!")
            return
        if not validate_username(username):
            st.error("Username hanya boleh menggunakan huruf dan angka")
            return
        if not validate_email(email):
            st.error("Format email tidak valid!")
            return
        if not validate_password(password):
            st.error("Panjang password minimal 8 karakter")
            return
        else:
            with st.spinner("Membuat akun..."):
                email_enc = encrypt_aes(email, master_key)
                success = register_user(
                    username, password, email_enc, caesar_key, vigenere_key
                )
            if success:
                st.success("Akun berhasil dibuat! Silakan login.")
                st.session_state["page"] = "login"
            else:
                st.error("Username atau email sudah digunakan!")

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
