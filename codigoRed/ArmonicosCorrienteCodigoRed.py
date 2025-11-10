import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def ArmonicosCorriente():
    with st.container():
            rutaTablaDescriptivasTHDCorriente=Datos["ArmonicosCorriente"]["ArmonicosITabla"]
            TablaDescriptivasTHDCorriente=Tabla("Descripción THD Corriente",rutaTablaDescriptivasTHDCorriente)
            TablaDescriptivasTHDCorriente.construirContenedor()
    with st.expander(label="Gráficas THD Corriente"):
        with st.container():
            rutaImagenTHDCorriente=Datos["ArmonicosCorriente"]["ArmonicosITiempo"]
            ImagenTHDCorriente=Imagenes("THD Corriente Serie de Tiempo",rutaImagenTHDCorriente)
            ImagenTHDCorriente.ConstruirImagen()
        with st.container():
            rutaImagenTHDCorrienteDistr=Datos["ArmonicosCorriente"]["ArmonicosIDistr"]
            ImagenTHDCorrienteDistr=Imagenes("THD Corriente Distribución",rutaImagenTHDCorrienteDistr)
            ImagenTHDCorrienteDistr.ConstruirImagen()
    with st.expander(label="THD Corriente por línea"):
        with st.container():
            rutaImagenTHDCorrienteDistrL1=Datos["ArmonicosCorriente"]["ArmonicosIL1"]
            ImagenTHDCorrienteDistrL1=Imagenes("THD Corriente L1",rutaImagenTHDCorrienteDistrL1)
            ImagenTHDCorrienteDistrL1.ConstruirImagen()
        with st.container():
            rutaImagenTHDCorrienteDistrL2=Datos["ArmonicosCorriente"]["ArmonicosIL2"]
            ImagenTHDCorrienteDistrL2=Imagenes("THD Corriente L2",rutaImagenTHDCorrienteDistrL2)
            ImagenTHDCorrienteDistrL2.ConstruirImagen()
        with st.container():
            rutaImagenTHDCorrienteDistrL3=Datos["ArmonicosCorriente"]["ArmonicosIL3"]
            ImagenTHDCorrienteDistrL3=Imagenes("THD Corriente L3",rutaImagenTHDCorrienteDistrL3)
            ImagenTHDCorrienteDistrL3.ConstruirImagen()
        