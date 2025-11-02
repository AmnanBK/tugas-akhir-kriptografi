import streamlit as st
from database.notes import add_note
from utils.encryption_utils import super_encrypt
from datetime import datetime

st.set_page_config(page_title="Tambah Catatan", layout="wide")
caesar_key = int(st.session_state["user_settings"]["caesar_key"])
vigenere_key = st.session_state["user_settings"]["vigenere_key"]
rsa_private = st.session_state["user_settings"]["rsa_private"]
rsa_public = st.session_state["user_settings"]["rsa_public"]
vault_key = st.session_state["user_settings"]["vault_key"]


def logout():
    st.session_state.clear()
    st.session_state["page"] = "login"
    st.rerun()


def show_sidebar():
    username = st.session_state.get("username", "UserDemo")
    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")
        st.divider()

        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("📝 Tambah Catatan", use_container_width=True):
            st.rerun()
        if st.button("🔒 Brankas Pribadi", use_container_width=True):
            st.switch_page("pages/4_File_Vault.py")
        if st.button("🖼️ Galeri Rahasia", use_container_width=True):
            st.switch_page("pages/5_Gallery.py")
        if st.button("⚙️ Pengaturan", use_container_width=True):
            st.switch_page("pages/6_Settings.py")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()


def show_add_note_form():
    st.title("📝 Tambah Catatan")
    st.divider()

    with st.form("add_note_form"):
        judul = st.text_input("🧾 Judul Catatan")
        isi = st.text_area("🖊️ Isi Catatan", height=200)
        submitted = st.form_submit_button("💾 Simpan Catatan")
        canceled = st.form_submit_button("↩️ Batal")

    if canceled:
        st.switch_page("pages/1_Dashboard.py")
        return

    if submitted:
        if not judul.strip() or not isi.strip():
            st.warning("⚠️ Judul dan isi catatan tidak boleh kosong!")
            return

        user_id = st.session_state.get("user_id")
        if not user_id:
            st.error("⚠️ User belum login!")
            return

        try:
            # Super encryption
            encrypted_content = super_encrypt(isi, caesar_key, vigenere_key, rsa_public)
            success = add_note(judul, encrypted_content, user_id)

            if success:
                st.success("✅ Catatan berhasil disimpan!")
                st.session_state["new_note"] = {
                    "judul": judul,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("❌ Gagal menyimpan catatan!")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat menyimpan catatan: {e}")


def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Silakan login terlebih dahulu!")
        st.switch_page("app")
        return

    show_sidebar()
    show_add_note_form()


if __name__ == "__main__":
    main()
