import streamlit as st
import pandas as pd
import requests
from streamlit_geolocation import streamlit_geolocation

# URL que te dio Google al implementar el Script
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx1zuQI3fY8V2vRvyvDDo72fmsOCaTfRYwMciUYRJ9HvwX8IjJ7yVZu9MerjK8pCrk/exec"

st.title("📍 Coordenadas JOL")

# 1. Tu maestra (cargada desde el repo)
df_maestra = pd.read_excel("maestra_clientes.xlsx")
asesor = st.selectbox("Seleccione asesor:", sorted(df_maestra['ASESOR'].unique().astype(str)))
cliente = st.selectbox("Seleccione cliente:", df_maestra[df_maestra['ASESOR']==asesor]['NOMBRE'].tolist())

# 2. Registrar
loc = streamlit_geolocation()
if st.button("✅ REGISTRAR"):
    datos = {"cliente": cliente, "asesor": asesor, "lat": loc['latitude'], "long": loc['longitude']}
    requests.post(WEB_APP_URL, json=datos)
    st.success("¡Registrado en tu hoja de cálculo!")

