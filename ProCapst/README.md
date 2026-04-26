# ProCapst

ProCapst (Property Capital Structure) adalah Aplikasi Berbasis Web untuk analisis dan prediksi Struktur Modal pada perusahaan properti.
Aplikasi ini dibangun menggunakan framework [Streamlit](https://streamlit.io/) yang interaktif dan mudah digunakan.

## Struktur Direktori

```text
ProCapst/
├── app.py                   # File utama aplikasi (konfigurasi dan routing UI Streamlit)
├── requirements.txt         # Daftar dependency package Python
├── data/                    # Tempat penyimpanan dataset mentah atau yang telah diproses
├── pickles-import/          # Tempat penyimpanan model terlatih dan objek machine learning (.pkl)
├── tabs/                    # Halaman/tab representasi antarmuka aplikasi
│   ├── __init__.py
│   ├── tab01_beranda.py     # Halaman beranda dengan informasi aplikasi
│   ├── tab02_master_data.py # Halaman tampilan data referensi 
│   ├── tab03_visualisasi_data.py # Halaman grafik dan eksplorasi data (EDA)
│   └── tab04_prediksi.py    # Logika dan halaman eksekusi prediksi menggunakan Machine Learning
└── utils/                   # Modul utilitas pendukung
    └── preprocessing.py     # Fungsi untuk pra-pemrosesan data sebelum pemodelan atau prediksi
```

## Fitur Utama

- **Beranda**: Menampilkan gambaran umum tentang tujuan aplikasi.
- **Master Data**: Menyediakan tampilan dan akses ke tabel data historis perusahaan properti.
- **Visualisasi Data**: Memberikan analisis dan insight berbentuk grafik interaktif.
- **Prediksi**: Menjalankan prediksi metrik struktur modal memanfaatkan parameter yang dimasukkan dan model Machine Learning.

## Persyaratan (Prerequisites)

- Python 3.7+
- Pip (Python Package Installer)

## Cara Instalasi dan Penggunaan

1. **Buka Terminal / Command Prompt** dan pastikan berada di direktori `ProCapst`.
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
   streamlit run app.py
   ```
5. **Akses Aplikasi**:
   Sistem biasanya akan otomatis membuka browser pada tautan: [http://localhost:8501](http://localhost:8501)

## Arsitektur Singkat
Aplikasi `ProCapst` menggunakan framework Streamlit untuk membangun UI yang dibagi menjadi beberapa tab modular di direktori `tabs/` agar kodenya lebih terstruktur. Data utama disimpan pada folder `data/` dan diproses dengan bantuan fungsi dari `utils/preprocessing.py`, sebelum dijalankan melalui model prediksi yang dimuat dari folder `pickles-import/`.