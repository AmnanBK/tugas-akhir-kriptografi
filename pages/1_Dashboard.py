import streamlit as st
from database.notes import get_all_notes, get_note_by_id, delete_note
from utils.encryption_utils import super_decrypt

st.set_page_config(page_title="Dashboard", layout="wide")


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
            st.rerun()
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


def show_dashboard():
    username = st.session_state.get("username", "UserDemo")
    user_id = st.session_state.get("user_id")

    st.title(f"📘 Dashboard - Selamat datang, {username}!")
    st.divider()

    notes = get_all_notes(user_id)
    if not notes:
        st.info("Belum ada catatan")
        return

    header_cols = st.columns([0.5, 3, 2, 2])
    header_cols[0].markdown("**No**")
    header_cols[1].markdown("**Judul**")
    header_cols[2].markdown("**Tanggal**")
    header_cols[3].markdown("**Aksi**")
    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    for i, note in enumerate(notes, 1):
        cols = st.columns([0.5, 3, 2, 2])
        cols[0].markdown(f"{i}")
        cols[1].markdown(f"{note['title']}")
        cols[2].markdown(f"{note['created_at']}")

        with cols[3]:
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("👁️", key=f"view{note['id']}"):
                    st.session_state["view_note"] = {
                        "id": note["id"],
                        "title": note["title"],
                        "encrypted_content": note["encrypted_content"],
                    }
                    st.switch_page("pages/3_View_Note.py")
            with c2:
                if st.button("✏️", key=f"edit_{note['id']}"):
                    st.session_state["edit_note_id"] = note["id"]
                    st.switch_page("pages/2_Add_Note.py")
            with c3:
                if st.button("🗑️", key=f"del_{note['id']}"):
                    if delete_note(note["id"], user_id):
                        st.success(f"Catatan '{note['title']}' berhasil dihapus!")
                        st.rerun()
                    else:
                        st.error("Gagal menghapus catatan!")

        st.markdown("<hr style='margin:2px 0;'>", unsafe_allow_html=True)

    st.markdown("---")
    st.write("Klik tombol ✏️ untuk edit atau 🗑️ untuk hapus catatan.")


def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Silakan login terlebih dahulu!")
        st.switch_page("app.py")
        return

    caesar_key = int(st.session_state["user_settings"]["caesar_key"])
    vigenere_key = st.session_state["user_settings"]["vigenere_key"]
    rsa_private = st.session_state["user_settings"]["rsa_private"]
    rsa_public = st.session_state["user_settings"]["rsa_public"]
    vault_key = st.session_state["user_settings"]["vault_key"]

    show_sidebar()
    show_dashboard()


if __name__ == "__main__":
    main()
