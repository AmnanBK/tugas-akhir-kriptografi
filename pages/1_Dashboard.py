import streamlit as st
import pandas as pd
from datetime import datetime


def main():
    st.set_page_config(page_title="Dashboard", layout="wide")

    # Simulasi login sementara
    username = st.session_state.get("username", "UserDemo")

    # Sidebar
    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")

        st.divider()
        # Tombol navigasi
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("1_Dashboard.py")
        if st.button("📝 Tambah Catatan", use_container_width=True):
            st.switch_page("2_Add_Note.py")
        if st.button("🔒 Brankas Pribadi", use_container_width=True):
            st.switch_page("4_File_Vault.py")
        if st.button("🖼️ Galeri Rahasia", use_container_width=True):
            st.switch_page("pages/5_Gallery.py")
        if st.button("⚙️ Pengaturan", use_container_width=True):
            st.switch_page("pages/6_Settings.py")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")

    # Dashboard
    st.title(f"📘 Dashboard - Selamat datang, {username}!")
    st.divider()

    # Daftar catatan
    header_cols = st.columns([0.5, 3, 2, 2])
    header_cols[0].markdown("**No**")
    header_cols[1].markdown("**Judul**")
    header_cols[2].markdown("**Tanggal**")
    header_cols[3].markdown("**Aksi**")

    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    # Dummy data
    notes = [
        {"id": 1, "judul": "Catatan Rahasia A", "tanggal": "2025-11-02"},
        {"id": 2, "judul": "Catatan Harian B", "tanggal": "2025-11-01"},
        {"id": 3, "judul": "Daftar Ide", "tanggal": "2025-10-30"},
    ]

    if not notes:
        st.info("Belum ada catatan")
        return

    # Loop isi tabel
    for i, note in enumerate(notes, 1):
        cols = st.columns([0.5, 3, 2, 2])
        cols[0].markdown(f"{i}")
        cols[1].markdown(f"{note['judul']}")
        cols[2].markdown(f"{note['tanggal']}")

        # Tombol aksi
        with cols[3]:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.button("👁️", key=f"view{note['id']}", help="Lihat Catatan")
            with c2:
                st.button("✏️", key=f"edit_{note['id']}", help="Edit Catatan")
            with c3:
                st.button("🗑️", key=f"del_{note['id']}", help="Hapus Catatan")

        st.markdown("<hr style='margin:2px 0;'>", unsafe_allow_html=True)

    st.markdown("---")
    st.write("Klik tombol ✏️ untuk edit atau 🗑️ untuk hapus catatan.")


if __name__ == "__main__":
    main()
