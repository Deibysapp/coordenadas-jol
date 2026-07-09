import streamlit as st
import pandas as pd
import os
from streamlit_geolocation import streamlit_geolocation

# Configuración de página
st.set_page_config(page_title="Sistema de Coordenadas", layout="wide")

st.title("📍 Registro de Coordenadas de Clientes")

# Carga de la maestra de clientes
# Asegúrate de que este archivo exista en la misma carpeta
if not os.path.exists('MAESTRA_CLIENTES.xlsx'):
    st.error("No se encuentra el archivo 'MAESTRA_CLIENTES.xlsx'. Por favor súbelo.")
    st.stop()

df_maestra = pd.read_excel('MAESTRA_CLIENTES.xlsx')

# Selección de asesor
asesor = st.selectbox("Selecciona tu código de asesor:", 
                      ["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V10", "V11", "V12"])

# Filtrar clientes por asesor
clientes_filtrados = df_maestra[df_maestra['Vendedor'] == asesor]['Nombre_Cliente'].tolist()
cliente = st.selectbox("Selecciona el cliente:", clientes_filtrados)

# Obtener ubicación
col1, col2 = st.columns(2)
with col1:
    location = streamlit_geolocation()

if location and location['latitude']:
    lat = location['latitude']
    lon = location['longitude']
    st.success(f"Ubicación obtenida: {lat}, {lon}")
    
    if st.button("Guardar Coordenadas"):
        nueva_fila = {
            'Asesor': asesor,
            'Cliente': cliente,
            'Latitud': lat,
            'Longitud': lon
        }
        
        # Guardar en archivo persistente
        archivo_salida = 'MIC_COORDENADAS.xlsx'
        if os.path.exists(archivo_salida):
            df_existente = pd.read_excel(archivo_salida)
            df_actualizado = pd.concat([df_existente, pd.DataFrame([nueva_fila])], ignore_index=True)
        else:
            df_actualizado = pd.DataFrame([nueva_fila])
        
        df_actualizado.to_excel(archivo_salida, index=False)
        st.success(f"✅ Coordenadas guardadas para {cliente}")
        st.rerun()

# Botón para descargar el reporte
if os.path.exists('MIC_COORDENADAS.xlsx'):
    with open("MIC_COORDENADAS.xlsx", "rb") as f:
        st.download_button("📥 Descargar Reporte Excel", f, "Reporte_Coordenadas.xlsx")

