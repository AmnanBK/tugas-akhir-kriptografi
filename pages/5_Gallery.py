import streamlit as st
import os
from datetime import datetime
from PIL import Image
from utils.auth_utils import check_login
from utils.ui_components import show_sidebar, hide_default_sidebar()
from crypto.lsb_stego import encode_text_into_image, decode_text_from_image
from database.gallery import (
    add_stego_image,
    get_all_stego_images,
    delete_stego_image,
)


st.set_page_config(page_title="Galeri Rahasia", layout="wide")

GALLERY_DIR = os.path.join("data", "images")
os.makedirs(GALLERY_DIR, exist_ok=True)


def save_temp_image(uploaded_file) -> str:
    os.makedirs(GALLERY_DIR, exist_ok=True)
    temp_path = os.path.join(
        GALLERY_DIR, f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    )
    image = Image.open(uploaded_file).convert("RGB")
    image.save(temp_path)
    return temp_path


def encode_and_save_stego(title, temp_input, secret_msg, user_id):
    try:
        output_name = f"stego_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = os.path.join(GALLERY_DIR, output_name)

        success = encode_text_into_image(temp_input, output_path, secret_msg)
        os.remove(temp_input)

        if not success:
            st.error("❌ Gagal menyembunyikan pesan ke dalam gambar.")
            return

        with open(output_path, "rb") as f:
            image_data = f.read()

        add_stego_image(title, image_data, user_id)
        show_encode_success(output_path, output_name, image_data)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")


def show_encode_success(output_path, output_name, image_data):
    st.success("✅ Pesan berhasil disembunyikan dan disimpan!")
    st.image(output_path, caption="Gambar dengan pesan tersembunyi", use_container_width=True)
    st.download_button(
        label="⬇️ Unduh Gambar Stego",
        data=image_data,
        file_name=output_name,
        mime="image/png",
    )


def decode_stego_image(stego_file):
    try:
        temp_path = os.path.join(GALLERY_DIR, "temp_decode.png")
        with open(temp_path, "wb") as f:
            f.write(stego_file.read())

        decoded_text = decode_text_from_image(temp_path)
        os.remove(temp_path)

        if decoded_text:
            st.text_area("Pesan Rahasia Terbaca:", value=decoded_text, height=200)
        else:
            st.warning("Tidak ditemukan pesan rahasia atau gambar tidak valid.")
    except Exception as e:
        st.error(f"Gagal membaca pesan: {e}")


def show_gallery_list(user_id):
    st.subheader("🗂️ Koleksi Gambar Rahasia Anda")
    images = get_all_stego_images(user_id)

    if not images:
        st.info("Belum ada gambar yang disimpan.")
        return

    for img in images:
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            st.markdown(f"**{img['title']}**")
            st.caption(f"📅 {img['created_at']}")
        with col2:
            st.image(img["file_path"], width=150)
        with col3:
            if st.button("🗑️ Hapus", key=f"del_{img['id']}"):
                delete_stego_image(img["id"], user_id)
                st.rerun()


def show_gallery():
    user_id = st.session_state.get("user_id")
    st.title("🖼️ Galeri Rahasia")
    st.divider()

    tab1, tab2 = st.tabs(["📤 Sembunyikan Pesan", "📥 Baca Pesan"])

    with tab1:
        st.subheader("📤 Sembunyikan Pesan dalam Gambar")
        title = st.text_input("Judul Gambar", placeholder="Contoh: Rahasia Liburan")
        image_file = st.file_uploader("Unggah Gambar", type=["png", "jpg", "bmp"])
        secret_msg = st.text_area(
            "Pesan Rahasia", placeholder="Tulis pesan rahasia di sini..."
        )

        if st.button("🔒 Proses dan Simpan"):
            if not (image_file and secret_msg.strip() and title.strip()):
                st.warning("⚠️ Lengkapi semua kolom terlebih dahulu!")
            else:
                temp_input = save_temp_image(image_file)
                encode_and_save_stego(title, temp_input, secret_msg, user_id)

    with tab2:
        st.subheader("📥 Baca Pesan dari Gambar Stego")
        stego_file = st.file_uploader("Unggah Gambar Stego", type=["png", "jpg", "bmp"])

        if st.button("🔍 Decode Pesan"):
            if not stego_file:
                st.warning("⚠️ Unggah gambar stego terlebih dahulu!")
            else:
                decode_stego_image(stego_file)

    st.divider()
    show_gallery_list(user_id)


def main():
    check_login()
    hide_default_sidebar()
    show_sidebar()
    show_gallery()


if __name__ == "__main__":
    main()
