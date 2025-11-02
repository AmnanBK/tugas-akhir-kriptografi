import streamlit as st
from database.users import login_user, register_user

st.set_page_config(page_title="Secret Diary App", page_icon="🔐", layout="centered")


# Fungsi halaman
def show_login():
    st.title("🔐 Secret Diary App")
    st.subheader("Masuk untuk membuka brankas rahasiamu 🔑")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.write("Login...")
        # user = login_user(username, password)
        # if user:
        #     st.success("Login berhasil! Mengarahkan ke dashboard...")
        #     st.switch_page("pages/1_Dashboard.py")
        # else:
        #     st.error("Username atau password salah!")

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
        st.write("Login...")
        # if register_user(username, password, email):
        #     st.success("Akun berhasil dibuat! Silakan login.")
        #     st.session_state["page"] = "login"
        #     st.rerun()
        # else:
        #     st.error("Email atau sudah digunakan!")

    st.markdown("---")
    st.caption("Sudah punya akun?")
    if st.button("🔑 Kembali ke Login"):
        st.session_state["page"] = "login"
        st.rerun()


def show_dashboard():
    st.title(f"Selamat datang, {st.session_state['username']} 👋")
    st.success("Kamu berhasil login.")
    if st.button("Logout"):
        # logout()
        st.rerun()


# Main
def main():
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