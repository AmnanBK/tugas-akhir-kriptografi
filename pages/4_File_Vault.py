import streamlit as st
import os
from datetime import datetime
from crypto.rc4 import rc4_encrypt_decrypt
from database.files import add_file, get_all_files, get_file_by_id, delete_file


def main():
    st.set_page_config(page_title="Brankas Pribadi", layout="wide")

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠️ Silakan login terlebih dahulu!")
        st.switch_page("app")
        return

    username = st.session_state.get("username", "UserDemo")
    user_id = st.session_state.get("user_id")

    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")
        st.divider()

        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("📝 Tambah Catatan", use_container_width=True):
            st.switch_page("pages/2_Add_Note.py")
        if st.button("🔒 Brankas Pribadi", use_container_width=True):
            st.rerun()
        if st.button("🖼️ Galeri Rahasia", use_container_width=True):
            st.switch_page("pages/5_Gallery.py")
        if st.button("⚙️ Pengaturan", use_container_width=True):
            st.switch_page("pages/6_Settings.py")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("app.py")

    st.title("🔒 Brankas Pribadi")
    st.divider()

    uploaded_file = st.file_uploader("📁 Pilih file untuk diunggah")
    key = st.text_input("🔑 Masukkan Kunci RC4", type="password")

    if st.button("💾 Enkripsi & Simpan"):
        if not uploaded_file or not key:
            st.warning("⚠️ Pilih file dan masukkan kunci terlebih dahulu.")
        else:
            try:
                file_bytes = uploaded_file.read()
                encrypted_bytes = rc4_encrypt_decrypt(file_bytes, key.encode())

                encrypted_name = uploaded_file.name

                success = add_file(encrypted_name, encrypted_bytes, user_id)
                if success:
                    st.success(
                        f"✅ File '{uploaded_file.name}' berhasil dienkripsi dan disimpan!"
                    )
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan file ke database.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat enkripsi: {e}")

    st.divider()
    st.subheader("📂 Daftar File Anda")

    files = get_all_files(user_id)
    if not files:
        st.info("Belum ada file yang disimpan di brankas Anda.")
    else:
        for file in files:
            with st.expander(f"📄 {file['file_name']}"):
                st.write(f"🕒 Tanggal Upload: {file['created_at']}")
                key_input = st.text_input(
                    "Masukkan Kunci RC4 untuk Dekripsi",
                    type="password",
                    key=f"key_{file['id']}",
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔓 Dekripsi & Unduh", key=f"dec_{file['id']}"):
                        if not key_input:
                            st.warning("⚠️ Harap masukkan kunci terlebih dahulu.")
                        else:
                            try:
                                file_path = file["file_path"]
                                with open(file_path, "rb") as f:
                                    encrypted_data = f.read()

                                decrypted_data = rc4_encrypt_decrypt(
                                    encrypted_data, key_input.encode()
                                )

                                st.download_button(
                                    label="⬇️ Unduh File Dekripsi",
                                    data=decrypted_data,
                                    file_name=file["file_name"].replace(".enc", ""),
                                    key=f"dl_{file['id']}",
                                )
                                st.success("✅ Dekripsi berhasil!")
                            except Exception as e:
                                st.error(f"❌ Gagal dekripsi: {e}")

                with col2:
                    if st.button("🗑️ Hapus", key=f"del_{file['id']}"):
                        if delete_file(file["id"], user_id):
                            st.success(
                                f"🗑️ File '{file['file_name']}' berhasil dihapus."
                            )
                            st.rerun()
                        else:
                            st.error("❌ Gagal menghapus file.")


if __name__ == "__main__":
    main()
