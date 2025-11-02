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

    # Tambah catatan
    st.title("📝 Tambah Catatan")
    st.divider()
    
    # Form tambah catatan
    with st.form("add_note_form"):
        judul = st.text_input("🧾 Judul Catatan")
        isi = st.text_area("🖊️ Isi Catatan", height=200)
        submitted = st.form_submit_button("💾 Simpan Catatan")
        canceled = st.form_submit_button("↩️ Batal")

    if canceled:
        st.switch_page("pages/1_Dashboard.py")

    if submitted:
        if not judul or not isi:
            st.warning("⚠️ Judul dan isi catatan tidak boleh kosong!")
            return

        # try:
        #     # proses enkripsi
        #     encrypted_text = super_encrypt(isi)

        #     # simpan ke database
        #     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     user_id = st.session_state.get("user_id", 1)  # sementara default 1
        #     insert_note(user_id, judul, encrypted_text, now)

        #     # tampilkan pesan sukses
        #     st.success("✅ Catatan berhasil disimpan!")
        #     st.session_state["new_note"] = {
        #         "judul": judul,
        #         "cipher": encrypted_text,
        #         "tanggal": now
        #     }

        #     # redirect ke halaman detail
        #     st.switch_page("pages/3_View_Note.py")

        # except Exception as e:
        #     st.error(f"❌ Gagal menyimpan catatan: {e}")

if __name__ == "__main__":
    main() 