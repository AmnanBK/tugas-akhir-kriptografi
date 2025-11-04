import json
import streamlit as st
from utils.encryption_utils import super_decrypt
from utils.auth_utils import check_login
from utils.ui_components import show_sidebar, hide_default_sidebar

st.set_page_config(page_title="Detail Catatan", layout="wide")


def show_view_note():
    rsa_private = st.session_state["user_settings"]["rsa_private"]
    vigenere_key = st.session_state["user_settings"]["vigenere_key"]
    caesar_key = int(st.session_state["user_settings"]["caesar_key"])

    note = st.session_state.get("view_note")

    if not note:
        st.warning("⚠️ Tidak ada catatan yang dipilih!")
        st.stop()

    encrypted_content = json.loads(note["encrypted_content"])

    st.title("📝 Detail Catatan")
    st.subheader(note["title"])
    st.divider()

    st.markdown("### 🔒 Ciphertext")
    st.text_area(
        "Teks terenkripsi", str(note["encrypted_content"]), height=150, disabled=True
    )

    if st.button("🔓 Dekripsi Otomatis"):
        try:
            decrypted_text = super_decrypt(
                encrypted_content,
                rsa_private=rsa_private,
                vigenere_key=vigenere_key,
                caesar_key=caesar_key,
            )
            st.success("✅ Dekripsi berhasil!")
            st.text_area("Plaintext", decrypted_text, height=200)
        except Exception as e:
            st.error(f"❌ Gagal dekripsi: {e}")


def main():
    check_login()
    hide_default_sidebar()
    show_sidebar()
    show_view_note()


if __name__ == "__main__":
    main()
