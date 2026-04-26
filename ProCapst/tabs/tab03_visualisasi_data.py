import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from sklearn.preprocessing import MinMaxScaler
from utils.preprocessing import TopEmitenTransformer

def render(df_raw=None, df_hasil=None, variabel_x=None, variabel_y=None, model_der=None, model_tdr=None, emiten_top=None):

    st.header("Visualisasi Data Panel")
    st.markdown("Visualisasi di bawah ini menggunakan data rasio dari tabel **HASIL PERHITUNGAN**.")
    
    # Layout 2x2 untuk visualisasi
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # --- A. LINE CHART (Tren Utang) ---
    with row1_col1:
        st.subheader("📈 Tren Struktur Modal")
        lc_target = st.selectbox("Pilih Indikator:", variabel_y, key='lc_target')
        lc_emiten = st.multiselect("Adu Emiten (Max 3 disarankan):", options=st.session_state['df_hasil']['Emiten'].unique(), default=st.session_state['df_hasil']['Emiten'].unique()[:3], key='lc_emiten')
        
        if lc_emiten:
            df_lc = st.session_state['df_hasil'][st.session_state['df_hasil']['Emiten'].isin(lc_emiten)].sort_values(by='Tahun')
            fig_line = px.line(df_lc, x='Tahun', y=lc_target, color='Emiten', markers=True,
                               title=f"Perbandingan {lc_target} Lintas Tahun", template='plotly_dark')
            fig_line.update_xaxes(dtick=1) # Agar tahun tidak tampil desimal
            st.plotly_chart(fig_line, config={'displayModeBar': True, 'responsive': True})
        else:
            st.warning("Pilih minimal 1 emiten.")

    # --- B. RADAR CHART (Spider Web) ---
    with row1_col2:
        st.subheader("🕸️ Spider Web (Fundamental Komparatif)")
        rc_emiten = st.multiselect("Pilih Emiten untuk Diadu:", options=st.session_state['df_hasil']['Emiten'].unique(), default=st.session_state['df_hasil']['Emiten'].unique()[:2], key='rc_emiten')
        
        # Kecualikan tahun 2025 pada pilihan Spider Web karena indikatornya bernilai NaN
        opts_tahun_radar = [y for y in st.session_state['df_hasil']['Tahun'].unique() if y != 2025]
        rc_tahun = st.selectbox("Pilih Tahun:", options=opts_tahun_radar, index=max(0, len(opts_tahun_radar)-1))
        
        if rc_emiten:
            df_rc = st.session_state['df_hasil'][(st.session_state['df_hasil']['Emiten'].isin(rc_emiten)) & (st.session_state['df_hasil']['Tahun'] == rc_tahun)][['Emiten'] + variabel_x].dropna()
            
            if not df_rc.empty:
                # Wajib Standardisasi 0-1 agar bentuk web tidak rusak
                scaler = MinMaxScaler()
                df_scaled = df_rc.copy()
                
                # Fit scaler pada keseluruhan data (bukan cuma emiten terpilih) agar proporsi antar-emiten adil
                scaler.fit(st.session_state['df_hasil'][variabel_x]) 
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
                st.plotly_chart(fig_radar, config={'displayModeBar': True, 'responsive': True})
            else:
                st.info("Data untuk emiten dan tahun yang dipilih tidak tersedia.")
        else:
            st.warning("Pilih minimal 1 emiten.")

    # --- C. HEATMAP CORRELATION ---
    with row2_col1:
        st.subheader("🔥 Heatmap Korelasi")
        corr_type = st.radio("Jenis Korelasi:", ["Overall (Antar Semua Data)", "Within (Demeaned - Karakter Panel)"])
        
        # Buang tahun 2025 agar NaN dari target/features 2025 tidak merusak matriks korelasi
        df_korelasi = st.session_state['df_hasil'][st.session_state['df_hasil']['Tahun'] != 2025].copy()
        
        if corr_type == "Overall (Antar Semua Data)":
            corr_matrix = df_korelasi[variabel_x + variabel_y].corr()
        else:
            # Menghitung Within Correlation (Demeaned by Emiten)
            df_demeaned = df_korelasi.copy()
            for col in variabel_x + variabel_y:
                # Mengurangi nilai setiap observasi dengan rata-rata emiten tersebut
                df_demeaned[col] = df_demeaned.groupby('Emiten')[col].transform(lambda x: x - x.mean())
            corr_matrix = df_demeaned[variabel_x + variabel_y].corr()

        fig_heat = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1, template='plotly_dark')
        st.plotly_chart(fig_heat, config={'displayModeBar': True, 'responsive': True})

    # --- D. SCATTER PLOT (Kuadran Interaktif) ---
    with row2_col2:
        st.subheader("📍 Peta Sebaran (Bubble Plot)")
        col_sc1, col_sc2 = st.columns(2)
        with col_sc1:
            sc_x = st.selectbox("Sumbu X (Fundamental):", variabel_x, index=0)
        with col_sc2:
            sc_y = st.selectbox("Sumbu Y (Target):", variabel_y, index=1)
            
        # Mengecualikan 2025 (krn metrik fundamental-nya NaN semua)
        df_scatter = st.session_state['df_hasil'][st.session_state['df_hasil']['Tahun'] != 2025].dropna(subset=[sc_x, sc_y, 'SIZ'])
        fig_scatter = px.scatter(df_scatter, x=sc_x, y=sc_y, size='SIZ', color='Emiten', hover_name='Emiten',
                                 animation_frame='Tahun', size_max=40,
                                 title=f"{sc_x} vs {sc_y} (Ukuran Bola = SIZ)", template='plotly_dark')
        st.plotly_chart(fig_scatter, config={'displayModeBar': True, 'responsive': True})

# ==========================================
# TAB 4: PREDIKSI & SIMULASI MACHINE LEARNING
# ==========================================

