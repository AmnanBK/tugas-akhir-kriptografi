import streamlit as st
from database.users import login_user, register_user
from database.settings import get_user_settings

st.set_page_config(page_title="Secret Diary App", page_icon="🔐", layout="centered")


def logout():
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"
    for key in ["username", "user_id"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# Fungsi halaman
def show_login():
    st.title("🔐 Secret Diary App")
    st.subheader("Masuk untuk membuka brankas rahasiamu 🔑")

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

    email = st.text_input("E-mail Baru")
    username = st.text_input("Username Baru")
    password = st.text_input("Password", type="password")

    if st.button("Daftar"):
        if username.strip() == "" or password.strip() == "" or email.strip() == "":
            st.error("Semua field wajib diisi!")
        else:
            with st.spinner("Membuat akun..."):
                success = register_user(username, password, email)
            if success:
                st.success("Akun berhasil dibuat! Silakan login.")
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error("Username atau email sudah digunakan!")

    st.markdown("---")
    st.caption("Sudah punya akun?")
    if st.button("🔑 Kembali ke Login"):
        st.session_state["page"] = "login"
        st.rerun()


def show_dashboard():
    st.title(f"Selamat datang, {st.session_state['username']} 👋")
    st.success("Kamu berhasil login.")
    if st.button("Logout"):
        logout()


# Main
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # init_session()
    page = st.session_state.get("page", "login")

    if st.session_state.get("logged_in", False):
        st.switch_page("pages/1_Dashboard.py")
    elif page == "login":
        show_login()
    elif page == "register":
        show_register()


if __name__ == "__main__":
    main()
