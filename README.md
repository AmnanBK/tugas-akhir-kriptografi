# tugas-akhir-kriptografi - Private Vault App

Private Vault App adalah aplikais berbasis **Streamlit** yang berfungsi untuk menyimpan file dan data pribadi dengan aman menggunakan implementasi berbagai **algoritma kriptografi klasik dan modern**, seperti RC4, Caesar Cipher, Vigenère Cipher, dan RSA.

---

## Fitur Utama

**Autentikasi Pengguna**
- Sistem login dan register dengan penyimpanan data terenkripsi.
- Validasi input untuk menjaga keamanan dan integritas data.

**Enkripsi & Dekrispi Catatan**
- Enkripsi catatan dengan super enkripsi (caesar->vigenere->rsa)
- Pengguna dapat menyimpan catatannya dengan

**Enkripsi & Dekripsi File**
- Enkripsi file dengan **RC4 Cipher** sebelum disimpan ke storage.
- Catatan akan dienkripsi sebelum masuk database

**Manajemen Kunci**
- Menyimpan kunci enkripsi (Caesar, Vigenère, dan RSA) secara aman.
- Kunci disimpan di database dalam bentuk terenkripsi menggunakan **AES128**.

**Steganografi File Gambar**
- Upload, lihat, unduh, dan hapus file gambar untuk steganografi dan menyimpan pesan rahasia
- Steganografi menggunakan algoritma LSB (Least Significant Bit)

---

## Teknologi yang Digunakan

| Komponen | Teknologi |
|----------|------------|
| Bahasa Pemrograman | Python 3.12 |
| Framework UI | Streamlit |
| Database | SQLite3 |
| Enkripsi | RC4, Caesar Cipher, Vigenère Cipher, RSA, AES |

---

## Instalasi & Setup

### 1. Clone Repository
```bash
git clone https://github.com/username/brankas-pribadi.git
cd brankas-pribadi
```

### 2.Buat Virtual Environment (Opsional)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Buat File .env
Tambahkan variabel berikut dalam file .env:
```
MASTER_KEY="16byteslongkey!!"
```

### 5. Inisialisasi Database
```bash
python database/db_init.py
```

### 6. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan berjalan pada: http://localhost:8501

---

## Struktur Proyek
```bash
Private-Vault-App/
│
├── app.py
│
├── crypto/
│   ├── aes128.py
│   ├── caesar.py
│   ├── hash_sha256.py
│   ├── lsb_stego.py
│   ├── rc4.py
│   └── rsa.py
│
├── database/
│   ├── db_connection.py
│   ├── db_init.py
│   ├── files.py
│   ├── gallery.py
│   ├── notes.py
│   ├── settings.py
│   └── users.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Add_Note.py
│   ├── 3_View_Note.py
│   ├── 4_File_Vault.py
│   ├── 5_Gallery.py
│   └── 6_Settings.py
│
├── utils/
│   ├── auth_utils.py
│   ├── encryption_utils.py
│   ├── ui_components.py
│   └── validators.py
│
├── .env
├── requirements.txt
└── README.md
```
