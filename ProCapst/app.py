import streamlit as st
import pandas as pd
import numpy as np
import joblib

from tabs import tab01_beranda, tab02_master_data, tab03_visualisasi_data, tab04_prediksi
from utils.preprocessing import TopEmitenTransformer

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="ProCapst Analytics", page_icon="🏢", layout="wide")

# ==========================================
# FUNGSI MEMUAT DATA (Dari Excel Asli)
# ==========================================
@st.cache_data
def load_data():
    try:
        df_raw = pd.read_excel('data/Property_Data.xlsx', sheet_name='RAW DATA')
        df_hasil = pd.read_excel('data/Property_Data.xlsx', sheet_name='HASIL PERHITUNGAN')
        return df_raw, df_hasil
    except FileNotFoundError:
        st.error("File 'Property_Data.xlsx' tidak ditemukan! Pastikan file Excel tersebut berada di folder yang sama dengan aplikasi.")
        st.stop()

# ==========================================
# FUNGSI MEMUAT MODEL
# ==========================================
@st.cache_resource
def load_models():
    try:
        model_der = joblib.load('pickles-import/03_model_rf_der.pkl')
        model_tdr = joblib.load('pickles-import/03_model_rf_tdr.pkl')
        emiten_top = joblib.load('pickles-import/02_model1_features_emiten.pkl')
        return model_der, model_tdr, emiten_top
    except Exception as e:
        st.error(f"Gagal memuat model: {e}. Pastikan file .pkl berada di folder yang benar.")
        st.stop()

# Load dataset
df_raw, df_hasil = load_data()

# Load models
model_der, model_tdr, emiten_top = load_models()

# Session State
if 'df_hasil' not in st.session_state:
    st.session_state['df_hasil'] = df_hasil.copy()

# Mendefinisikan Variabel
variabel_x = ['ROE', 'TAN', 'LIQ', 'GRW', 'SIZ', 'TAX', 'AGE', 'NDTS']
variabel_y = ['DER', 'TDR']

# ==========================================
# JUDUL DASHBOARD
# ==========================================
st.title("🏢 ProCapst Analytics")
st.markdown("Platform Analitik Cerdas untuk Struktur Modal Perusahaan Properti")

# Membuat 4 Tab
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Beranda", "🗄️ Master Data", "📊 Visualisasi Data", "✨ Prediksi"])

with tab1:
    tab01_beranda.render()

with tab2:
    tab02_master_data.render(df_raw=df_raw, df_hasil=df_hasil)

with tab3:
    tab03_visualisasi_data.render(variabel_x=variabel_x, variabel_y=variabel_y)

with tab4:
    tab04_prediksi.render(variabel_x=variabel_x, variabel_y=variabel_y, model_der=model_der, model_tdr=model_tdr, emiten_top=emiten_top)
