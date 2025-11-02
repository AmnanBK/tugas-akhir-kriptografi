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
    st.set_page_config(page_title="Pengaturan", layout="wide")

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

    # Pengaturan
    st.title("⚙️ Pengaturan")
    st.divider()

    st.subheader("Master Key")
    master_key = st.text_input("Masukkan Master Key", type="password")
    if st.button("Simpan Key"):
        if master_key:
            # enkripsi key di sini jika perlu
            # update_master_key(username, master_key)
            st.success("Master Key tersimpan!")
        else:
            st.warning("Master Key tidak boleh kosong.")

    st.divider()

    # Ganti password
    st.subheader("Ganti Password")
    old_pass = st.text_input("Password Lama", type="password")
    new_pass = st.text_input("Password Baru", type="password")
    if st.button("Simpan"):
        if old_pass and new_pass:
            # hash password lama/baru sesuai sistem login
            # old_hashed = hash_password(old_pass)
            # new_hashed = hash_password(new_pass)
            # success = update_user_password(username, old_hashed, new_hashed)
            success = True
            if success:
                st.success("Password berhasil diperbarui!")
            else:
                st.error("Password lama salah.")
        else:
            st.warning("Password tidak boleh kosong!")

    st.divider()

    # Hapus akun
    st.subheader("Hapus Akun")
    st.warning("⚠️ Akun akan dihapus secara permanen")
    if st.button("Hapus Akun", type="secondary"):
        st.write("Apakah kamu yakin ingin menghapus akun ini?")
            # delete_user(username)
            # st.success("Akun berhasil dihapus!")
            # st.session_state.clear()
            # st.experimental_rerun()  # atau arahkan ke halaman login

if __name__ == "__main__":
    main()
