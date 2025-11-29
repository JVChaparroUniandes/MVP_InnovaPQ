import streamlit as st
from codigoRed.codigoRed import CodigoRed
from cargaDatos.cargaDatos2 import CargarDatos2

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Carga de Reportes PQ",
    layout="wide"
)


# Lee el query param "report_id" de la URL
# Ejemplo: https://mi-app-review.com/?report_id=123-456-789&pagina=codigored
report_id = st.query_params.get("report_id")
pagina=st.query_params.get("pagina")


if pagina=="codigored":
    CodigoRed(report_id)
elif pagina=="cargar":
    CargarDatos2()
else:
    st.write("No Hay pagina especificada")