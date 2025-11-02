import json
import streamlit as st
from utils.encryption_utils import super_decrypt

st.set_page_config(page_title="Detail Catatan", layout="wide")
caesar_key = int(st.session_state["user_settings"]["caesar_key"])
vigenere_key = st.session_state["user_settings"]["vigenere_key"]
rsa_private = st.session_state["user_settings"]["rsa_private"]
rsa_public = st.session_state["user_settings"]["rsa_public"]
vault_key = st.session_state["user_settings"]["vault_key"]
encrypted_content = json.loads(st.session_state["view_note"]["encrypted_content"])


def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Silakan login terlebih dahulu!")
        st.switch_page("app")
        return

    username = st.session_state.get("username", "UserDemo")
    user_settings = st.session_state.get("user_settings", {})

    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")
        st.divider()
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
            st.switch_page("app")

    note = st.session_state.get("view_note")
    if not note:
        st.warning("⚠️ Tidak ada catatan yang dipilih!")
        st.stop()

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


if __name__ == "__main__":
    main()
