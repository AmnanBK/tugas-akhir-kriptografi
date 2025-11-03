import streamlit as st
from utils.auth_utils import check_login
from utils.ui_components import show_sidebar
from crypto.rc4 import rc4_encrypt_decrypt
from database.files import add_file, get_all_files, delete_file

st.set_page_config(page_title="Brankas Pribadi", layout="wide")


def encrypt_and_save_file(uploaded_file, key, user_id):
    try:
        file_bytes = uploaded_file.read()
        encrypted_bytes = rc4_encrypt_decrypt(file_bytes, key.encode())
        success = add_file(uploaded_file.name, encrypted_bytes, user_id)
        return success
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat enkripsi: {e}")
        return False


def decrypt_file(file_record, key_input):
    try:
        file_path = file_record["file_path"]
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = rc4_encrypt_decrypt(encrypted_data, key_input.encode())
        st.download_button(
            label="⬇️ Unduh File Dekripsi",
            data=decrypted_data,
            file_name=file_record["file_name"],
            key=f"dl_{file_record['id']}",
        )
        st.success("✅ File telah didekripsi!")
    except Exception as e:
        st.error(f"❌ Gagal dekripsi: {e}")


def show_file_item(file, user_id):
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
                    decrypt_file(file, key_input)

        with col2:
            if st.button("🗑️ Hapus", key=f"del_{file['id']}"):
                if delete_file(file["id"], user_id):
                    st.success(f"🗑️ File '{file['file_name']}' berhasil dihapus.")
                    st.rerun()
                else:
                    st.error("❌ Gagal menghapus file.")


def show_file_vault():
    user_id = st.session_state.get("user_id")
    st.title("🔒 Brankas Pribadi")
    st.divider()

    uploaded_file = st.file_uploader("📁 Pilih file untuk diunggah")
    key = st.text_input("🔑 Masukkan Kunci RC4", type="password")

    if st.button("💾 Enkripsi & Simpan"):
        if not uploaded_file or not key:
            st.warning("⚠️ Pilih file dan masukkan kunci terlebih dahulu.")
        else:
            if encrypt_and_save_file(uploaded_file, key, user_id):
                st.success(
                    f"✅ File '{uploaded_file.name}' berhasil dienkripsi dan disimpan!"
                )
                st.rerun()
            else:
                st.error("❌ Gagal menyimpan file ke database.")

    st.divider()
    st.subheader("📂 Daftar File Anda")

    files = get_all_files(user_id)
    if not files:
        st.info("Belum ada file yang disimpan di brankas Anda.")
    else:
        for file in files:
            show_file_item(file, user_id)


def main():
    check_login()
    show_sidebar()
    show_file_vault()


if __name__ == "__main__":
    main()
