import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    st.set_page_config(page_title="Detail Catatan", layout="wide")

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

    # Dummy note
    note = {
        "judul": "Catatan Rahasia A",
        "ciphertext": "Nkg gzkk gz znk yzxotm znk ot ul znk Rgkx...",
    }

    # Tambah catatan
    st.title("📝 Detail Catatan")
    st.subheader(note["judul"])
    st.divider()
    
    # Ciphertext
    st.markdown("### 🔒 Ciphertext")
    st.text_area(
        "Teks terenkripsi",
        note["ciphertext"],
        height=150,
        disabled=True
    )

    # Input key dekripsi
    st.markdown("### 🔑 Dekripsi Catatan")
    key_caesar = st.text_input("Key Caesar", max_chars=10)
    key_vigenere = st.text_input("Key Vigenere", max_chars=20)
    rsa_private_key = st.text_input("Private Key RSA")

    if st.button("🔓 Dekripsi Catatan", use_container_width=True):
        if not key_caesar or not key_vigenere or not rsa_private_key:
            st.warning("⚠️ Harap isi semua key terlebih dahulu.")
        else:
            decrypted_text = "(hasil dekripsi dummy)"
            st.success("✅ Dekripsi berhasil!")
            st.text_area("Plaintext", decrypted_text, height=150)

if __name__ == "__main__":
    main() 