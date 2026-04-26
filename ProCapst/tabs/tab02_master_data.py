import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from sklearn.preprocessing import MinMaxScaler
from utils.preprocessing import TopEmitenTransformer

def render(df_raw=None, df_hasil=None, variabel_x=None, variabel_y=None, model_der=None, model_tdr=None, emiten_top=None):

    st.header("Eksplorasi Master Data")
    st.markdown("Gunakan filter di bawah ini. Tabel RAW DATA dan HASIL PERHITUNGAN akan tersinkronisasi otomatis.")
    
    # Buat copy dari df_raw agar tidak memodifikasi objek asli dan menghindari SettingWithCopyWarning
    df_raw = df_raw.copy()
    
    # Forward fill kolom Emiten untuk mengatasi merge cell dari Excel
    df_raw['Emiten'] = df_raw['Emiten'].ffill()

    # Hapus data kosong dan tahun 2019 dari raw data serta buat copy baru
    df_raw = df_raw.dropna(subset=['Tahun']).copy()
    df_raw['Tahun'] = df_raw['Tahun'].astype(int)
    if 'Year Listed' in df_raw.columns:
        df_raw['Year Listed'] = df_raw['Year Listed'].fillna(0).astype(int)
    if 'AGE' in df_raw.columns:
        df_raw['AGE'] = df_raw['AGE'].fillna(0).astype(int)
    df_raw = df_raw[df_raw['Tahun'] != 2019]

    # Ambil list unik Emiten dan Tahun (menggunakan st.session_state['df_hasil'] sebagai acuan)
    list_emiten = st.session_state['df_hasil']['Emiten'].unique()
    list_tahun = st.session_state['df_hasil']['Tahun'].unique()
    
    # Filter Data
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_emiten = st.multiselect("Filter Emiten:", options=list_emiten, default=list_emiten)
    with col_f2:
        selected_tahun = st.multiselect("Filter Tahun:", options=list_tahun, default=list_tahun)
    
    # Terapkan Filter pada kedua dataframe
    df_raw_filtered = df_raw[(df_raw['Emiten'].isin(selected_emiten)) & (df_raw['Tahun'].isin(selected_tahun))]
    df_hasil_filtered = st.session_state['df_hasil'][(st.session_state['df_hasil']['Emiten'].isin(selected_emiten)) & (st.session_state['df_hasil']['Tahun'].isin(selected_tahun))]
    
    # Tampilkan Tabel
    tab_raw, tab_hasil = st.tabs(["📑 RAW Data", "🧮 Hasil Perhitungan"])
    
    with tab_raw:
        # Konfigurasi format teks untuk rentang kolom tertentu
        raw_cols = df_raw_filtered.columns
        cols_to_format = raw_cols[2:-2]
        
        # Menggunakan Pandas Styler untuk memastikan pemisah ribuan (koma) dan prefix Rp tampil secara konsisten
        def format_rupiah(val):
            if pd.isna(val):
                return ""
            return f"-Rp.{abs(val):,.0f}" if val < 0 else f"Rp.{val:,.0f}"

        format_dict = {col: format_rupiah for col in cols_to_format}
        df_raw_styled = df_raw_filtered.style.format(format_dict)

        st.dataframe(df_raw_styled, width='stretch', hide_index=True)
        # Tombol Download CSV untuk RAW Data
        csv_raw = df_raw_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download RAW Data (CSV)", data=csv_raw, file_name='Procapst_RAW_Data.csv', mime='text/csv')

    with tab_hasil:
        st.dataframe(df_hasil_filtered, width='stretch', hide_index=True)
        # Tombol Download CSV untuk Hasil Perhitungan
        csv_hasil = df_hasil_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Hasil Perhitungan (CSV)", data=csv_hasil, file_name='Procapst_Hasil_Perhitungan.csv', mime='text/csv')

# ==========================================
# TAB 3: VISUALISASI DATA
# ==========================================
