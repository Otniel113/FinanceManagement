# FleksFin

Aplikasi Berbasis Web untuk Memprediksi Fleksibilitas Finansial (FFR) Perusahaan.
Aplikasi ini dibangun menggunakan framework [Flask](https://flask.palletsprojects.com/) dengan fitur penghitungan *Cash Ratio Output* (CRO).

## Struktur Direktori

```
FleksFin/
├── app.py                   # File utama aplikasi (routing dan logic backend)
├── requirements.txt         # Daftar dependency package Python
├── static/                  # File statis (CSS, JavaScript, gambar)
│   ├── css/style.css
│   └── js/script.js
├── templates/               # Layout HTML 
│   └── index.html           # Halaman utama aplikasi
└── utils/                   # Modul utilitas untuk validasi dll.
    ├── __init__.py
    └── input_validator.py   # Logika validasi input user (Simple & Full mode)
```

## Fitur Utama

- **Simple Mode**: Memasukkan parameter dasar untuk menghitung CRO.
- **Full Mode**: Memasukkan parameter lebih spesifik untuk menganalisis fleksibilitas finansial.
- **Prediksi Fleksibilitas**: Menentukan apakah perusahaan terindikasi fleksibel secara finansial berdasarkan rata-rata industri (Dummy threshold CRO = 0.12).

## Persyaratan (Prerequisites)

- Python 3.7+
- Pip (Python Package Installer)

## Cara Instalasi dan Penggunaan

1. **Buka Terminal / Command Prompt** dan pastikan berada di direktori `FleksFin`.
2. **(Opsional) Aktifkan Virtual Environment** (direkomendasikan):
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. **Instal Library yang Dibutuhkan**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Jalankan Aplikasi**:
   ```bash
   python app.py
   ```
5. **Akses Aplikasi**:
   Buka browser dan kunjungi tautan: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Arsitektur Singkat
Aplikasi `FleksFin` ini memisahkan layer presentasi di dalam `templates/` dan `static/`, sedangkan logic aplikasi ditangani oleh `app.py` (controller) dan validasi diproses oleh `utils/input_validator.py`. Evaluasi didorong oleh nilai indikator CRO dan batas nilai (threshold) yang mengidentifikasikan bantalan kas, di mana CRO >= threshold dianggap **Fleksibel**. 
