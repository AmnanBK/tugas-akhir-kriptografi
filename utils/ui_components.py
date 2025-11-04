import streamlit as st
from utils.auth_utils import logout


def hide_default_sidebar():
    hide_nav_style = """
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """
    st.markdown(hide_nav_style, unsafe_allow_html=True)


def show_sidebar():
    username = st.session_state.get("username", "UserDemo")

    with st.sidebar:
        st.markdown("## 🔐 Private Vault")
        st.write(f"👤 **{username}**")
        st.divider()

        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("app.py")

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
            logout()
