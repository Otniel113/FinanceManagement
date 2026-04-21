# FinanceManagement

Repositori ini berisi kumpulan analisis kuantitatif dari bidang studi Manajemen dengan peminatan Finansial. Proyek ini merupakan hasil kolaborasi dengan mahasiswa jurusan terkait, yang difokuskan pada pengujian hipotesis dan pencarian faktor-faktor yang paling berpengaruh pada struktur serta fleksibilitas keuangan suatu perusahaan.

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
> ⚠️ **DISCLAIMER:** Terdapat sedikit perbedaan versi antara data yang tercantum di literatur referensi dengan data yang digunakan di sini, sehingga hasil akhirnya akan sedikit berbeda.

#### 📝 Notebooks:

*   **[01_Regresi_Logistik.ipynb](Faktor-Fleksibilitas-Keuangan/01_Regresi_Logistik.ipynb)**
    Melakukan pendekatan kuantitatif menggunakan metode Regresi Logistik sesuai dengan referensi utama. Tahapan analisis meliputi pengenalan masalah, eksplorasi data (EDA), Uji Asumsi Logistik (seperti pengecekan Multikolinearitas menggunakan VIF), dan Uji Hipotesis. Hasil dari pemodelan ini menunjukkan bahwa variabel **Cash Holding (CRO)** berpengaruh paling signifikan terhadap fleksibilitas keuangan (FFR).

*   **[02_Metode_Lain.ipynb](Faktor-Fleksibilitas-Keuangan/02_Metode_Lain.ipynb)**
    Eksplorasi tingkat lanjut untuk menguji tingkat pengaruh setiap variabel menggunakan berbagai metode alternatif. Metode yang diterapkan dalam notebook ini meliputi:
    - **Uji Korelasi**: Point-Biserial dan Rank-Biserial.
    - **Uji Beda Rata-rata**: Independent T-Test, Welch's T-Test, dan Mann-Whitney U.
    - **Machine Learning (Ensemble Methods)**: Random Forest & XGBoost.
    - **Analisis Fitur Ensemble (Feature Importance)**: Gini Importance, SHAP values, Permutation Importance, dan Recursive Feature Elimination (RFE/RFECV).
    - **SelectKBest**: ANOVA dan Mutual Information

*   **[03_Model_Prediksi.ipynb](Faktor-Fleksibilitas-Keuangan/03_Model_Prediksi.ipynb)**
    *(Coming Soon)* Rencana untuk membangun model prediksi klasifikasi untuk menebak tingkat fleksibilitas keuangan perusahaan di masa depan.

---

### 2. Determinan-Capital-Structure
Studi kasus pada perusahaan-perusahaan sektor properti.
*(Coming Soon)*