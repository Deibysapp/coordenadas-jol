import streamlit as st
import pandas as pd
import os
import io
from streamlit_geolocation import streamlit_geolocation

# Configuración de página
st.set_page_config(page_title="Coordenadas JOL", layout="wide")

DB_FILE = "MIC COORDENADAS.xlsx"

def cargar_db():
    if os.path.exists(DB_FILE):
        # engine='openpyxl' soluciona el ValueError
        df = pd.read_excel(DB_FILE, engine='openpyxl', dtype=str)
        df.columns = df.columns.str.strip().str.upper()
        return df
    else:
        st.error(f"El archivo {DB_FILE} no está en la carpeta.")
        return pd.DataFrame()

df_maestra = cargar_db()

st.title("📍 Coordenadas JOL - Sistema de Gestión")

if not df_maestra.empty:
    asesor = st.selectbox("Seleccione asesor:", sorted(df_maestra['ASESOR'].unique()))
    df_asesor = df_maestra[df_maestra['ASESOR'].astype(str).str.strip() == asesor]

    # Resaltado visual en verde
    def resaltar_fila(row):
        val_x = str(row.get('COORDENADA X', '0.00'))
        es_valido = val_x != "0.00" and val_x != "nan" and val_x != ""
        return ['background-color: #90EE90' if es_valido else ''] * len(row)

    st.dataframe(df_asesor.style.apply(resaltar_fila, axis=1), use_container_width=True)

    cliente = st.selectbox("Seleccionar cliente:", df_asesor['NOMBRE'].tolist())
    location = streamlit_geolocation()

    if location and location['latitude']:
        if st.button("Guardar Coordenadas GPS"):
            lat, lon = str(location['latitude']), str(location['longitude'])
            try:
                idx = df_maestra[df_maestra['NOMBRE'] == cliente].index[0]
                df_maestra.at[idx, 'COORDENADA X'] = lat
                df_maestra.at[idx, 'COORDENADA Y'] = lon
                df_maestra.to_excel(DB_FILE, index=False, engine='openpyxl')
                st.success("✅ ¡Coordenadas guardadas!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}. Asegúrate de cerrar el archivo Excel.")

    # Descarga de reporte
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_maestra.to_excel(writer, index=False)
    st.download_button("📥 Descargar Reporte Excel", buffer.getvalue(), "Reporte_Final.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

