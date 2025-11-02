import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE_DIR = "data/files"
os.makedirs(FILE_DIR, exist_ok=True)

# RC4 Dummy
def rc4_encrypt_decrypt(key, data):
    # untuk contoh, kita return data apa adanya
    return data

def main():
    st.set_page_config(page_title="Brankas Pribadi", layout="wide")

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

    # Brankas pribadi
    st.title("🔒 Brankas Pribadi")
    st.divider()

    uploaded_file = st.file_uploader("Pilih file untuk diunggah")
    key = st.text_input("Kunci RC4", type="password")

    if st.button("Enkripsi dan Simpan"):
        if uploaded_file and key:
            data = uploaded_file.read()
            encrypted_data = rc4_encrypt_decrypt(key, data)
            save_path = os.path.join(FILE_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(encrypted_data)
            st.success(f"File {uploaded_file.name} berhasil disimpan terenkripsi!")
        else:
            st.warning("⚠️ Pilih file dan masukkan key terlebih dahulu.")

    st.divider()
    st.subheader("Daftar File Tersimpan")

    files = os.listdir(FILE_DIR)
    if not files:
        st.info("Belum ada file di brankas.")
    else:
        for fname in files:
            cols = st.columns([4,1])
            cols[0].markdown(fname)
            with cols[1]:
                if st.button("Dekripsi", key=f"download_{fname}"):
                    file_path = os.path.join(FILE_DIR, fname)
                    with open(file_path, "rb") as f:
                        encrypted_data = f.read()
                    decrypted_data = rc4_encrypt_decrypt(key, encrypted_data)

                    st.download_button(
                        label="⬇️ Unduh File",
                        data=decrypted_data,
                        file_name=fname,
                        key=f"dl_{fname}"
                    )

if __name__ == "__main__":
    main()
