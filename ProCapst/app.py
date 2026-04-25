import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="ProCapst Analytics", page_icon="🏢", layout="wide")

# ==========================================
# FUNGSI MEMUAT DATA (Dari Excel Asli)
# ==========================================
@st.cache_data
def load_data():
    """
    Membaca data langsung dari file Excel menggunakan sheet_name masing-masing.
    Pastikan file 'Property_Data.xlsx' berada di folder yang sama dengan script ini.
    """
    try:
        df_raw = pd.read_excel('Property_Data.xlsx', sheet_name='RAW DATA')
        df_hasil = pd.read_excel('Property_Data.xlsx', sheet_name='HASIL PERHITUNGAN')
        return df_raw, df_hasil
    except FileNotFoundError:
        st.error("File 'Property_Data.xlsx' tidak ditemukan! Pastikan file Excel tersebut berada di folder yang sama dengan aplikasi.")
        st.stop()

# Load dataset
df_raw, df_hasil = load_data()

# Mendefinisikan Variabel
variabel_x = ['ROE', 'TAN', 'LIQ', 'GRW', 'SIZ', 'TAX', 'AGE', 'NDTS']
variabel_y = ['DER', 'TDR']

# ==========================================
# JUDUL DASHBOARD
# ==========================================
st.title("🏢 ProCapst Analytics")
st.markdown("Platform Analitik Cerdas untuk Struktur Modal Perusahaan Properti")

# Membuat 3 Tab
tab1, tab2, tab3 = st.tabs(["🏠 Beranda", "🗄️ Master Data", "📊 Visualisasi Data"])

# ==========================================
# TAB 1: BERANDA
# ==========================================
with tab1:
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
with tab2:
    st.header("Eksplorasi Master Data")
    st.markdown("Gunakan filter di bawah ini. Tabel RAW DATA dan HASIL PERHITUNGAN akan tersinkronisasi otomatis.")
    
    # Forward fill kolom Emiten untuk mengatasi merge cell dari Excel
    df_raw['Emiten'] = df_raw['Emiten'].ffill()

    # Hapus data kosong dan tahun 2019 dari raw data
    df_raw = df_raw.dropna(subset=['Tahun'])
    df_raw['Tahun'] = df_raw['Tahun'].astype(int)
    if 'Year Listed' in df_raw.columns:
        df_raw['Year Listed'] = df_raw['Year Listed'].fillna(0).astype(int)
    if 'AGE' in df_raw.columns:
        df_raw['AGE'] = df_raw['AGE'].fillna(0).astype(int)
    df_raw = df_raw[df_raw['Tahun'] != 2019]

    # Ambil list unik Emiten dan Tahun (menggunakan df_hasil sebagai acuan)
    list_emiten = df_hasil['Emiten'].unique()
    list_tahun = df_hasil['Tahun'].unique()
    
    # Filter Data
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_emiten = st.multiselect("Filter Emiten:", options=list_emiten, default=list_emiten)
    with col_f2:
        selected_tahun = st.multiselect("Filter Tahun:", options=list_tahun, default=list_tahun)
    
    # Terapkan Filter pada kedua dataframe
    df_raw_filtered = df_raw[(df_raw['Emiten'].isin(selected_emiten)) & (df_raw['Tahun'].isin(selected_tahun))]
    df_hasil_filtered = df_hasil[(df_hasil['Emiten'].isin(selected_emiten)) & (df_hasil['Tahun'].isin(selected_tahun))]
    
    # Tampilkan Tabel
    tab_raw, tab_hasil = st.tabs(["📑 RAW Data", "🧮 Hasil Perhitungan"])
    
    with tab_raw:
        # Konfigurasi format teks untuk rentang kolom tertentu
        raw_cols = df_raw_filtered.columns
        cols_to_format = raw_cols[2:-2]
        
        # Menggunakan Pandas Styler untuk memastikan pemisah ribuan (koma) dan prefix Rp tampil secara konsisten
        format_dict = {col: "Rp.{:,.0f}" for col in cols_to_format}
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
with tab3:
    st.header("Visualisasi Data Panel")
    st.markdown("Visualisasi di bawah ini menggunakan data rasio dari tabel **HASIL PERHITUNGAN**.")
    
    # Layout 2x2 untuk visualisasi
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # --- A. LINE CHART (Tren Utang) ---
    with row1_col1:
        st.subheader("📈 Tren Struktur Modal")
        lc_target = st.selectbox("Pilih Indikator:", variabel_y, key='lc_target')
        lc_emiten = st.multiselect("Adu Emiten (Max 3 disarankan):", options=df_hasil['Emiten'].unique(), default=df_hasil['Emiten'].unique()[:3], key='lc_emiten')
        
        if lc_emiten:
            df_lc = df_hasil[df_hasil['Emiten'].isin(lc_emiten)].sort_values(by='Tahun')
            fig_line = px.line(df_lc, x='Tahun', y=lc_target, color='Emiten', markers=True,
                               title=f"Perbandingan {lc_target} Lintas Tahun", template='plotly_dark')
            fig_line.update_xaxes(dtick=1) # Agar tahun tidak tampil desimal
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("Pilih minimal 1 emiten.")

    # --- B. RADAR CHART (Spider Web) ---
    with row1_col2:
        st.subheader("🕸️ Spider Web (Fundamental Komparatif)")
        rc_emiten = st.multiselect("Pilih Emiten untuk Diadu:", options=df_hasil['Emiten'].unique(), default=df_hasil['Emiten'].unique()[:2], key='rc_emiten')
        rc_tahun = st.selectbox("Pilih Tahun:", options=df_hasil['Tahun'].unique(), index=len(df_hasil['Tahun'].unique())-1) # Default tahun terakhir
        
        if rc_emiten:
            df_rc = df_hasil[(df_hasil['Emiten'].isin(rc_emiten)) & (df_hasil['Tahun'] == rc_tahun)][['Emiten'] + variabel_x]
            
            if not df_rc.empty:
                # Wajib Standardisasi 0-1 agar bentuk web tidak rusak
                scaler = MinMaxScaler()
                df_scaled = df_rc.copy()
                
                # Fit scaler pada keseluruhan data (bukan cuma emiten terpilih) agar proporsi antar-emiten adil
                scaler.fit(df_hasil[variabel_x]) 
                df_scaled[variabel_x] = scaler.transform(df_rc[variabel_x])
                
                fig_radar = go.Figure()
                for index, row in df_scaled.iterrows():
                    fig_radar.add_trace(go.Scatterpolar(
                        r=row[variabel_x].values.tolist() + [row[variabel_x].values[0]], # Tutup garis polygon
                        theta=variabel_x + [variabel_x[0]],
                        fill='toself',
                        name=row['Emiten']
                    ))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, title=f"Kekuatan Fundamental {rc_tahun}", template='plotly_dark')
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("Data untuk emiten dan tahun yang dipilih tidak tersedia.")
        else:
            st.warning("Pilih minimal 1 emiten.")

    # --- C. HEATMAP CORRELATION ---
    with row2_col1:
        st.subheader("🔥 Heatmap Korelasi")
        corr_type = st.radio("Jenis Korelasi:", ["Overall (Antar Semua Data)", "Within (Demeaned - Karakter Panel)"])
        
        if corr_type == "Overall (Antar Semua Data)":
            corr_matrix = df_hasil[variabel_x + variabel_y].corr()
        else:
            # Menghitung Within Correlation (Demeaned by Emiten)
            df_demeaned = df_hasil.copy()
            for col in variabel_x + variabel_y:
                # Mengurangi nilai setiap observasi dengan rata-rata emiten tersebut
                df_demeaned[col] = df_demeaned.groupby('Emiten')[col].transform(lambda x: x - x.mean())
            corr_matrix = df_demeaned[variabel_x + variabel_y].corr()

        fig_heat = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1, template='plotly_dark')
        st.plotly_chart(fig_heat, use_container_width=True)

    # --- D. SCATTER PLOT (Kuadran Interaktif) ---
    with row2_col2:
        st.subheader("📍 Peta Sebaran (Bubble Plot)")
        col_sc1, col_sc2 = st.columns(2)
        with col_sc1:
            sc_x = st.selectbox("Sumbu X (Fundamental):", variabel_x, index=0)
        with col_sc2:
            sc_y = st.selectbox("Sumbu Y (Target):", variabel_y, index=1)
            
        fig_scatter = px.scatter(df_hasil, x=sc_x, y=sc_y, size='SIZ', color='Emiten', hover_name='Emiten',
                                 animation_frame='Tahun', size_max=40,
                                 title=f"{sc_x} vs {sc_y} (Ukuran Bola = SIZ)", template='plotly_dark')
        st.plotly_chart(fig_scatter, use_container_width=True)
