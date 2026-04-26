import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from sklearn.preprocessing import MinMaxScaler
from utils.preprocessing import TopEmitenTransformer

def render(df_raw=None, df_hasil=None, variabel_x=None, variabel_y=None, model_der=None, model_tdr=None, emiten_top=None):

    st.header("Tentang ProCapst Analytics")
    st.write("""
    **ProCapst Analytics** (singkatan dari Property Capital Structure) adalah dashboard interaktif yang dirancang khusus untuk membedah, 
    menganalisis, dan mensimulasikan struktur modal (*Capital Structure*) pada industri properti. 
    Platform ini mengintegrasikan data historis rasio fundamental dengan pemodelan statistik tingkat lanjut. Prediksi menggunakan *machine learning* 
    Random Forest untuk prediksi rasio utang (DER dan TDR) di masa depan.
    """)
    
    st.divider()
    
    st.subheader("📚 Glosarium Indikator Keuangan")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Variabel Dependen (Target):**
        * **DER (Debt-to-Equity Ratio):** Rasio utang terhadap modal sendiri. Mengukur leverage dan risiko modal.
        * **TDR (Total Debt Ratio):** Proporsi total aset yang dibiayai oleh utang. Mengukur solvabilitas perusahaan.
        """)
    with col2:
        st.markdown("""
        **Variabel Independen:**
        * **ROE (Return on Equity):** Tingkat profitabilitas/keuntungan.
        * **TAN (Tangibility):** Rasio kepemilikan aset fisik/berwujud yang bisa dijadikan jaminan.
        * **LIQ (Liquidity):** Ketersediaan kas atau aset lancar jangka pendek.
        * **GRW (Growth):** Tingkat pertumbuhan aset perusahaan.
        * **SIZ (Size):** Skala/ukuran perusahaan (diukur dari Log Natural Total Aset).
        * **TAX (Tax Rate):** Beban pajak yang ditanggung. Berkaitan dengan taktik *Tax Shield*.
        * **AGE (Firm Age):** Umur perusahaan sejak berdiri/IPO.
        * **NDTS (Non-Debt Tax Shield):** Perlindungan pajak dari instrumen selain utang.
        """)

# ==========================================
# TAB 2: MASTER DATA
# ==========================================
