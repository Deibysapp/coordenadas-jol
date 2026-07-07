import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Coordenadas JOL", layout="centered")

if 'registros' not in st.session_state: st.session_state.registros = []

st.title("📍 Coordenadas JOL")

asesor_actual = st.selectbox("Seleccione su código de asesor:", 
                      ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12"])

archivo = st.file_uploader("Cargar base de clientes (Excel)", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo, dtype=str)
    df.columns = df.columns.str.strip().str.upper()
    df['ASESOR'] = df['ASESOR'].str.strip()
    
    df_filtrado = df[df['ASESOR'] == asesor_actual]
    
    if not df_filtrado.empty:
        busqueda = st.text_input("🔍 Buscador inteligente:")
        if busqueda:
            df_filtrado = df_filtrado[df_filtrado['NOMBRE'].str.contains(busqueda, case=False, na=False)]
        
        cliente_seleccionado = st.selectbox("Seleccione cliente:", df_filtrado['NOMBRE'].tolist())
        
        if st.button("Capturar Coordenada"):
            codigo_cliente = df_filtrado.loc[df_filtrado['NOMBRE'] == cliente_seleccionado, 'CODIGO'].values[0]
            nueva_entrada = {
                "CODIGO": codigo_cliente,
                "NOMBRE": cliente_seleccionado,
                "ASESOR": asesor_actual,
                "COORDENADA X": "7.7667", # Valor simulado, reemplazar por GPS luego
                "COORDENADA Y": "-72.2167"
            }
            st.session_state.registros.append(nueva_entrada)
            st.success(f"✅ Registrado: {cliente_seleccionado}")

# --- Exportar a Excel real ---
if st.session_state.registros:
    df_final = pd.DataFrame(st.session_state.registros)
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Reporte')
    
    st.download_button(
        label="📥 Descargar Reporte en Excel",
        data=buffer.getvalue(),
        file_name="reporte_coordenadas.xlsx",
        mime="application/vnd.ms-excel"
    )

st.markdown("---")
st.caption("Deibys Ibañes 2026")


