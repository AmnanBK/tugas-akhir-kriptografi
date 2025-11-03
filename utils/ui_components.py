import streamlit as st
from utils.auth_utils import logout


def show_sidebar():
    """Tampilkan sidebar navigasi umum."""
    username = st.session_state.get("username", "UserDemo")

    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")
        st.divider()

        # Navigasi utama
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
