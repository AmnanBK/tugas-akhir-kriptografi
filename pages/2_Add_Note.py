import streamlit as st
from database.notes import add_note, update_note, get_note_by_id
from utils.encryption_utils import super_encrypt, super_decrypt
from utils.auth_utils import check_login
from utils.ui_components import show_sidebar, hide_default_sidebar
from datetime import datetime

st.set_page_config(page_title="Tambah Catatan", layout="wide")


def show_add_edit_form():
    st.title("📝 Tambah / Edit Catatan")
    st.divider()

    edit_note_id = st.session_state.get("edit_note_id")
    user_id = st.session_state.get("user_id")
    rsa_private = st.session_state["user_settings"]["rsa_private"]
    rsa_public = st.session_state["user_settings"]["rsa_public"]
    vigenere_key = st.session_state["user_settings"]["vigenere_key"]
    caesar_key = int(st.session_state["user_settings"]["caesar_key"])

    default_judul = ""
    default_isi = ""

    if edit_note_id:
        note_data = get_note_by_id(edit_note_id, user_id)
        if note_data:
            default_judul = note_data["title"]
            default_isi = super_decrypt(
                note_data["content"], rsa_private, vigenere_key, caesar_key
            )

    with st.form("add_note_form"):
        judul_input = st.text_input("🧾 Judul Catatan", value=default_judul)
        isi_input = st.text_area("🖊️ Isi Catatan", value=default_isi, height=200)
        submitted = st.form_submit_button("💾 Simpan Catatan")
        canceled = st.form_submit_button("↩️ Batal")

    if canceled:
        if "edit_note_id" in st.session_state:
            del st.session_state["edit_note_id"]
        st.switch_page("pages/1_Dashboard.py")
        return

    if submitted:
        if not judul_input.strip() or not isi_input.strip():
            st.warning("⚠️ Judul dan isi catatan tidak boleh kosong!")
            return

        try:
            encrypted_content = super_encrypt(
                isi_input, caesar_key, vigenere_key, rsa_public
            )

            if edit_note_id:
                success = update_note(
                    edit_note_id, judul_input, encrypted_content, user_id
                )
                if success:
                    st.success("✅ Catatan berhasil diperbarui!")
                    del st.session_state["edit_note_id"]
                else:
                    st.error("❌ Gagal memperbarui catatan!")
            else:
                success = add_note(judul_input, encrypted_content, user_id)
                if success:
                    st.success("✅ Catatan berhasil disimpan!")
                    st.session_state["new_note"] = {
                        "judul": judul_input,
                        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                else:
                    st.error("❌ Gagal menyimpan catatan!")

            st.switch_page("pages/1_Dashboard.py")

        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat menyimpan catatan: {e}")


def main():
    check_login()
    hide_default_sidebar()
    show_sidebar()
    show_add_edit_form()


if __name__ == "__main__":
    main()
