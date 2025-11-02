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
    st.set_page_config(page_title="Galeri Rahasia", layout="wide")

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

    # Galeri Rahasia (Steganografi)
    st.title("🖼️ Galeri Rahasia")
    st.divider()
    mode = st.radio("Mode", ["Sembunyikan Pesan", "Baca Pesan"])

    if mode == "Sembunyikan Pesan":
        st.subheader("Sembunyikan Pesan")
        image_file = st.file_uploader("Unggah Gambar", type=["png", "jpg", "bmp"])
        secret_msg = st.text_area("Pesan Rahasia")
        if st.button("Proses"):
            # if image_file is not None and secret_msg.strip():
                # encode LSB
                # stego_image = encode_lsb(image_file, secret_msg)
                # st.image(stego_image, caption="Gambar dengan pesan tersembunyi")
                # # tombol download
                # st.download_button(
                #     label="⬇️ Unduh Gambar Stego",
                #     data=stego_image.getvalue(),  # assuming PIL image or BytesIO
                #     file_name="stego_image.png",
                #     mime="image/png"
                # )
            # else:
                st.warning("Silakan unggah gambar dan isi pesan!")

    elif mode == "Baca Pesan":
        st.subheader("Baca Pesan")
        stego_file = st.file_uploader("Unggah Gambar Stego", type=["png", "jpg", "bmp"])
        if st.button("Decode"):
            # if stego_file is not None:
            #     secret_msg = decode_lsb(stego_file)
            #     st.text_area("Pesan Rahasia", value=secret_msg, height=200)
            # else:
                st.warning("Silakan unggah gambar stego!")

if __name__ == "__main__":
    main()
