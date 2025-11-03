import streamlit as st
import os
from datetime import datetime
from PIL import Image
import io

from crypto.lsb_stego import encode_text_into_image, decode_text_from_image
from database.gallery import (
    add_stego_image,
    get_all_stego_images,
    delete_stego_image,
)


GALLERY_DIR = os.path.join("data", "images")
os.makedirs(GALLERY_DIR, exist_ok=True)


def main():
    st.set_page_config(page_title="Galeri Rahasia", layout="wide")

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Silakan login terlebih dahulu!")
        st.switch_page("app")
        return
    username = st.session_state.get("username", "UserDemo")
    user_id = st.session_state.get("user_id")

    with st.sidebar:
        st.markdown("## 🔐 Secret Diary")
        st.write(f"👤 **{username}**")

        st.divider()
        if st.button("🏠 Dashboard", width="stretch"):
            st.switch_page("pages/1_Dashboard.py")
        if st.button("📝 Tambah Catatan", width="stretch"):
            st.switch_page("pages/2_Add_Note.py")
        if st.button("🔒 Brankas Pribadi", width="stretch"):
            st.switch_page("pages/4_File_Vault.py")
        if st.button("🖼️ Galeri Rahasia", width="stretch"):
            st.switch_page("pages/5_Gallery.py")
        if st.button("⚙️ Pengaturan", width="stretch"):
            st.switch_page("pages/6_Settings.py")

        st.divider()
        if st.button("🚪 Logout", width="stretch"):
            st.session_state.clear()
            st.switch_page("app.py")

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
                try:
                    temp_input = os.path.join(
                        GALLERY_DIR,
                        f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.png",
                    )
                    image = Image.open(image_file).convert("RGB")
                    image.save(temp_input)

                    output_name = (
                        f"stego_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    output_path = os.path.join(GALLERY_DIR, output_name)

                    success = encode_text_into_image(
                        temp_input, output_path, secret_msg
                    )
                    os.remove(temp_input)

                    if success:
                        with open(output_path, "rb") as f:
                            image_data = f.read()

                        add_stego_image(title, image_data, user_id)

                        st.success("✅ Pesan berhasil disembunyikan dan disimpan!")
                        st.image(
                            output_path,
                            caption="Gambar dengan pesan tersembunyi",
                            width="stretch",
                        )

                        st.download_button(
                            label="⬇️ Unduh Gambar Stego",
                            data=image_data,
                            file_name=output_name,
                            mime="image/png",
                        )
                    else:
                        st.error("❌ Gagal menyembunyikan pesan ke dalam gambar.")

                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

    with tab2:
        st.subheader("📥 Baca Pesan dari Gambar Stego")
        stego_file = st.file_uploader("Unggah Gambar Stego", type=["png", "jpg", "bmp"])

        if st.button("🔍 Decode Pesan"):
            if not stego_file:
                st.warning("⚠️ Unggah gambar stego terlebih dahulu!")
            else:
                try:
                    temp_path = os.path.join(GALLERY_DIR, "temp_decode.png")
                    with open(temp_path, "wb") as f:
                        f.write(stego_file.read())

                    decoded_text = decode_text_from_image(temp_path)
                    os.remove(temp_path)

                    if decoded_text:
                        st.text_area(
                            "Pesan Rahasia Terbaca:", value=decoded_text, height=200
                        )
                    else:
                        st.warning(
                            "Tidak ditemukan pesan rahasia atau gambar tidak valid."
                        )

                except Exception as e:
                    st.error(f"Gagal membaca pesan: {e}")

    # TABEL GALERI USER
    st.divider()
    st.subheader("🗂️ Koleksi Gambar Rahasia Anda")

    images = get_all_stego_images(user_id)
    if not images:
        st.info("Belum ada gambar yang disimpan.")
    else:
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


if __name__ == "__main__":
    main()
