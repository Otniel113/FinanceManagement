import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from sklearn.preprocessing import MinMaxScaler
from utils.preprocessing import TopEmitenTransformer

def render(df_raw=None, df_hasil=None, variabel_x=None, variabel_y=None, model_der=None, model_tdr=None, emiten_top=None):

    st.header("🔮 Simulasi & Prediksi Machine Learning")
    
    # Model loaded via arguments from app.py
    if model_der is None or model_tdr is None or emiten_top is None:
        st.error("Model gagal dimuat dan diteruskan ke tab ini!")
        st.stop()

    fitur_der = ['ROE', 'TAN', 'LIQ', 'GRW', 'SIZ', 'TAX', 'AGE', 'NDTS', 'DER', 'Is_Top_Emiten']
    fitur_tdr = ['ROE', 'TAN', 'LIQ', 'GRW', 'SIZ', 'TAX', 'AGE', 'NDTS', 'TDR']

    st.divider()


    # ==========================================
    # FITUR 1: PREDIKSI MASSAL TAHUN 2025
    # ==========================================
    st.subheader("1. Proyeksi Massal Tahun 2025")
    st.markdown("Prediksi DER dan TDR tahun 2025 untuk seluruh emiten berdasarkan fundamental akhir tahun 2024.")
    
    if 2025 in st.session_state['df_hasil']['Tahun'].values:
        st.success("✅ Data proyeksi 2025 sudah berhasil ditambahkan ke Master Data!")
        # Menampilkan tabel 2025 saja
        df_2025_show = st.session_state['df_hasil'][st.session_state['df_hasil']['Tahun'] == 2025].dropna(axis=1, how='all')
        st.dataframe(df_2025_show, width='stretch', hide_index=True)
    else:
        if st.button("🚀 Prediksi Untuk Tahun 2025"):
            # Ambil data tahun terakhir sebelum 2025 sebagai baseline/prediktor
            tahun_terakhir = st.session_state['df_hasil'][st.session_state['df_hasil']['Tahun'] != 2025]['Tahun'].max()
            df_baseline = st.session_state['df_hasil'][st.session_state['df_hasil']['Tahun'] == tahun_terakhir].copy()
            
            # Tambahkan kolom Is_Top_Emiten
            df_baseline['Is_Top_Emiten'] = df_baseline['Emiten'].apply(lambda x: 1 if x in emiten_top else 0)
            
            # Lakukan Prediksi
            pred_der_2025 = model_der.predict(df_baseline[fitur_der])
            pred_tdr_2025 = model_tdr.predict(df_baseline[fitur_tdr])
            
            # Bentuk Dataframe Baru khusus 2025
            df_2025 = pd.DataFrame({
                'Emiten': df_baseline['Emiten'],
                'Tahun': 2025,
                'DER': pred_der_2025,
                'TDR': pred_tdr_2025
            })
            
            # Gabungkan ke Master Data di session_state dan urutkan agar baris 2025 berada tepat di bawah 2024 per Emiten
            st.session_state['df_hasil'] = pd.concat([st.session_state['df_hasil'], df_2025], ignore_index=True)
            st.session_state['df_hasil'] = st.session_state['df_hasil'].sort_values(by=['Emiten', 'Tahun']).reset_index(drop=True)
            
            st.rerun()

    st.divider()

    # ==========================================
    # FITUR 2: SIMULASI PREDIKSI CUSTOM (What-If)
    # ==========================================
    st.subheader("2. Simulasi Kustom (*What-If Analysis*)")
    st.markdown("Pilih satu rekam data emiten historis, ubah angkanya, dan lihat dampaknya terhadap DER & TDR.")
    
    # 2a. Pemilihan Baris Data Historis
    col_emiten, col_tahun = st.columns(2)
    with col_emiten:
        sim_emiten = st.selectbox("Pilih Emiten Baseline:", options=st.session_state['df_hasil']['Emiten'].unique())
    with col_tahun:
        # Filter tahun hanya yang memiliki data komplit (bukan tahun 2025 yang isinya NaN)
        df_komplit = st.session_state['df_hasil'].dropna(subset=variabel_x)
        sim_tahun = st.selectbox("Pilih Tahun Baseline:", options=df_komplit[df_komplit['Emiten'] == sim_emiten]['Tahun'].unique())
    
    # Tarik baris data berdasarkan pilihan user
    baris_terpilih = df_komplit[(df_komplit['Emiten'] == sim_emiten) & (df_komplit['Tahun'] == sim_tahun)].iloc[0]
    
    st.markdown(f"**Silakan modifikasi metrik fundamental untuk {sim_emiten} (Baseline: {sim_tahun}):**")
    
    # 2b. Form Pengisian Kustom
    with st.form("form_simulasi"):
        input_kustom = {}
        
        # Membuat form input menjadi 2 hingga 4 kolom agar tidak memanjang ke bawah
        cols = st.columns(4)
        for i, var in enumerate(variabel_x):
            nilai_asli = float(baris_terpilih[var])
            # Masukkan ke dalam dictionary agar formatnya gampang diubah jadi Dataframe
            input_kustom[var] = cols[i % 4].number_input(f"{var}", value=nilai_asli, step=0.01)
            
        submit_simulasi = st.form_submit_button("🔮 Hitung Prediksi Kustom")
        
        if submit_simulasi:
            # Tambahkan juga fitur turunan yang dipakai model
            input_kustom['DER'] = float(baris_terpilih['DER'])
            input_kustom['TDR'] = float(baris_terpilih['TDR'])
            input_kustom['Is_Top_Emiten'] = 1 if sim_emiten in emiten_top else 0
            
            # Ubah dictionary input user menjadi Dataframe 1 baris
            df_input = pd.DataFrame([input_kustom])
            
            # Prediksi dengan model (sesuaikan fiturnya)
            hasil_der = model_der.predict(df_input[fitur_der])[0]
            hasil_tdr = model_tdr.predict(df_input[fitur_tdr])[0]
            
            # Tampilkan Hasil Before-After
            st.markdown("### 📊 Hasil Simulasi")
            res_col1, res_col2 = st.columns(2)
            
            res_col1.metric(
                label="Prediksi DER Baru", 
                value=f"{hasil_der:.4f}", 
                delta=f"{(hasil_der - baris_terpilih['DER']):.4f} dari tahun {sim_tahun}",
                delta_color="inverse" # Merah jika utang naik, hijau jika turun
            )
            res_col2.metric(
                label="Prediksi TDR Baru", 
                value=f"{hasil_tdr:.4f}", 
                delta=f"{(hasil_tdr - baris_terpilih['TDR']):.4f} dari tahun {sim_tahun}",
                delta_color="inverse"
            )