import streamlit as st
from database.notes import get_all_notes, delete_note
from utils.auth_utils import check_login
from utils.ui_components import show_sidebar

st.set_page_config(page_title="Dashboard", layout="wide")


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
    check_login()
    show_sidebar()
    show_dashboard()


if __name__ == "__main__":
    main()
