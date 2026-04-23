# FinanceManagement

Repositori ini berisi kumpulan analisis kuantitatif dari bidang studi Manajemen dengan peminatan Finansial. Proyek ini merupakan hasil kolaborasi dengan mahasiswa jurusan terkait. Fokusnya adalah uji hipotesis untuk mencari pengaruh dan apa saja yang mempengaruhi dari fleksibilitas keuangan perusahaan FMCG menggunkana Regresi Logistik dan juga struktur model perusahaan properti menggunakan Analisis Panel.

---

## 📂 Studi Kasus

### 1. Faktor-Fleksibilitas-Keuangan
Studi kasus ini berfokus pada **perusahaan-perusahaan konsumsi *non-cyclicals* (FMCG)** di Indonesia. Tujuannya adalah untuk mencari faktor penentu dari **Fleksibilitas Keuangan (FFR)** berdasarkan sejumlah variabel independen, yaitu:
- **ROA** (Profitabilitas)
- **TAS** (Tangibility)
- **CRO** (Cash Holding)
- **DTR** (Struktur Modal)
- **RNR** (Retained Earnings)
- **LTA** (Ukuran Perusahaan)

**Referensi Utama:**
> D. A. Nugraha, S. Muchtar, and A. Abyantara, "Faktor penentu fleksibilitas keuangan perusahaan barang konsumsi di Indonesia," *Jurnal Ekonomi Trisakti*, vol. 5, no. 2, pp. 1181-1188, 2025, doi: [10.25105/v5i2.23180](https://doi.org/10.25105/v5i2.23180).

*Catatan: Dataset diperoleh secara primer dengan menghubungi Author secara langsung.*
> ⚠️ **DISCLAIMER:** Terdapat perbedaan versi antara data yang tercantum di literatur referensi dengan data yang digunakan di sini, sehingga hasil akhirnya akan ada perbedaan.

#### 📝 Notebooks:

*   **[01_Regresi_Logistik.ipynb](Faktor-Fleksibilitas-Keuangan/01_Regresi_Logistik.ipynb)**
    Melakukan pendekatan kuantitatif menggunakan metode Regresi Logistik sesuai dengan referensi utama. Tahapan analisis meliputi pengenalan masalah, eksplorasi data (EDA), Uji Asumsi Logistik (seperti pengecekan Multikolinearitas menggunakan VIF), dan Uji Hipotesis. Hasil dari pemodelan ini menunjukkan bahwa variabel **Cash Holding (CRO)** berpengaruh paling signifikan terhadap fleksibilitas keuangan (FFR).

*   **[02_Metode_Lain.ipynb](Faktor-Fleksibilitas-Keuangan/02_Metode_Lain.ipynb)**
    Eksplorasi tingkat lanjut untuk menguji tingkat pengaruh setiap variabel menggunakan berbagai metode alternatif. Metode yang diterapkan dalam notebook ini meliputi:
    - **Uji Korelasi**: Point-Biserial dan Rank-Biserial.
    - **Uji Beda Rata-rata**: Independent T-Test, Welch's T-Test, dan Mann-Whitney U.
    - **Random Forest dan XGBoost**: Feature Importance, SHAP values, Permutation Importance, dan Recursive Feature Elimination (RFE/RFECV).
    - **Regresi Logistik L1 LASSO**: Koefisien dengan penalti
    - **SelectKBest**: ANOVA dan Mutual Information
    
    Variabel **Cash Holding (CRO)** hampir selalu jadi variabel terpenting dari semua metode tersebut.

*   **[03_Model_Prediksi.ipynb](Faktor-Fleksibilitas-Keuangan/03_Model_Prediksi.ipynb)**
    Membangun model prediksi klasifikasi untuk menebak tingkat fleksibilitas keuangan (FFR) perusahaan. Model ini dibangun menggunakan algoritma **Regresi Logistik** (*Machine Learning*). Proses yang dilakukan mencakup pra-pemrosesan data (*Train-Test Split*), pencarian hyperparameter terbaik menggunakan GridSearchCV, dan evaluasi model (Akurasi, ROC-AUC, dll). Model yang dibangun ada 2: Pertama dengan memasukan seluruh 6 variabel, dan kedua hanya memasukan **CRO**. Didapatkan model terbaik adalah yang kedua. Model kemudian diekspor dan disimpan dalam bentuk file `.pkl` (`lr2_final_model.pkl`) sehingga siap untuk digunakan lebih lanjut (misal untuk *deployment* aplikasi).

---

### 2. Determinan-Capital-Structure
Studi kasus ini berfokus pada **perusahaan-perusahaan sektor properti** di Indonesia. Tujuannya adalah untuk mencari faktor penentu dari **Struktur Modal**, yang diukur menggunakan dua variabel dependen yaitu **Debt-to-Equity Ratio (DER)** dan **Total Debt Ratio (TDR)**. Variabel independen yang diuji meliputi:
- **ROE** (Profitabilitas)
- **TAN** (Struktur Aset Fisik / Tangibility)
- **LIQ** (Likuiditas)
- **GRW** (Pertumbuhan Perusahaan)
- **SIZ** (Ukuran Perusahaan)
- **TAX** (Beban Pajak)
- **AGE** (Umur Perusahaan)
- **NDTS** (Penghematan Pajak Selain Utang)

**Referensi Utama:**
> *(Dalam proses publikasi)* "Determinan of Capital Structure dari Perusahaan Properti"

*Catatan: Dataset diperoleh secara primer dengan menghubungi Author secara langsung.*

#### 📝 Notebooks:

*   **[01_Analisis_Panel.ipynb](Determinan-Capital-Structure/01_Analisis_Panel.ipynb)**
    Melakukan pendekatan kuantitatif menggunakan metode **Analisis Data Panel**. Tahapan yang dilakukan meliputi manipulasi dan penyusunan data panel, statistik deskriptif, visualisasi matriks korelasi (*Within-Entity* & *Between-Entity*), serta Pemilihan Model (Pengevulasian metode *Common Effect Model*, *Fixed Effect Model*, dan *Random Effect Model*) melalui instrumen Uji Spesifikasi seperti Uji Chow dan Uji Hausman. Dibangun 2 model yang pertama untuk prediksi **DER** dan yang kedua untuk prediksi **TDR**. Hasil akhir adalah beberapa faktor-faktor penentu yang signifikan dan seberapa besar pengaruhnya.

*   **[02_Linear_vs_Tree.ipynb](Determinan-Capital-Structure/02_Linear_vs_Tree.ipynb)**
    Membandingkan performa pendekatan statistik linear (Regresi Panel) dengan algoritma *Machine Learning* berbasis pohon (Random Forest Regressor). Evaluasi pemodelan dilakukan menggunakan metrik seperti skor OOB (*Out-Of-Bag*) R-Squared, RMSE, dan MAE untuk menangkap pola non-linear. Notebook ini juga membedah *Feature Importance* guna mencari perbandingan mengenai teori ekonometrika keuangan dengan realitas faktor pendorong di lapangan (seperti penemuan fenomena *Unobserved Heterogeneity* pada nama emiten dibandingkan sekadar urusan *tax shield*). Serta, menguji kembali variabel-variabel yang sebelumnya harus dibuang (seperti SIZ) akibat ketidakmampuan regresi linear dalam menangani multikolinearitas.

*   **03_Model_Prediksi.ipynb**
    *(Coming Soon)* Rencana untuk membangun model prediksi untuk menebak nilai **DER** dan **TDR** di tahun mendatang menggunakan algoritma **Random Forest Regressor** berdasarkan pola historis yang telah ditemukan.   