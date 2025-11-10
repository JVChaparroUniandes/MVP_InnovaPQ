import streamlit as st
from Modelos import Tabla
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def Cumplimiento():
    # --- Tabla cumplimiento ---
    with st.container():
        rutaTablaCumplimiento=Datos["CumplimientoRed"]["Principal"]
        TablaCumplimiento=Tabla("Tabla de cumplimiento",rutaTablaCumplimiento)
        TablaCumplimiento.construirContenedor()

    with st.expander(label="Cumplimiento de armónicos de corriente"):
        rutaTablaArmonicosP95=Datos["ArmonicosCorriente"]["ArmonicosITablaP95"]
        TablaArmonicosP95=Tabla("Niveles de armónicos de corriente (P95)",rutaTablaArmonicosP95)
        TablaArmonicosP95.construirContenedor()


    with st.expander(label="Límites aplicables"):
        rutaTablaAplicables=Datos["CumplimientoRed"]["limaplicables"]
        TablaAplicables=Tabla("Código de red al centro de carga",rutaTablaAplicables)
        TablaAplicables.construirContenedor()

        rutaTablaLimdatad=Datos["CumplimientoRed"]["limdatd"]
        TablaAplicables=Tabla("DATD y DAI",rutaTablaLimdatad)
        TablaAplicables.construirContenedor()