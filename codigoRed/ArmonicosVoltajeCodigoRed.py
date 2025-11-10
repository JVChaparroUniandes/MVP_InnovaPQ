import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def ArmonicosVoltaje():

    with st.container():
        rutaTablaDescriptivasTHDVoltaje=Datos["ArmonicosVoltaje"]["ArmonicosTabla"]
        TablaDescriptivasTHDVoltaje=Tabla("Descripción Armónicos Voltaje",rutaTablaDescriptivasTHDVoltaje)
        TablaDescriptivasTHDVoltaje.construirContenedor()

    with st.expander(label="Gráficas THD Voltaje"):
        
        with st.container():
            rutaImagenTHDVoltaje=Datos["ArmonicosVoltaje"]["ArmonicosTiempo"]
            ImagenTHDVoltaje=Imagenes("THD Voltaje Serie de Tiempo",rutaImagenTHDVoltaje)
            ImagenTHDVoltaje.ConstruirImagen()

        with st.container():
            rutaImagenTHDVoltajeDistr=Datos["ArmonicosVoltaje"]["ArmonicosDistr"]
            ImagenTHDVoltajeDistr=Imagenes("THD Voltaje Distribución",rutaImagenTHDVoltajeDistr)
            ImagenTHDVoltajeDistr.ConstruirImagen()

    with st.expander(label="THD Voltaje por línea"):
        with st.container():
            rutaImagenTHDVoltajeDistrL1=Datos["ArmonicosVoltaje"]["ArmonicosL1"]
            ImagenTHDVoltajeDistrL1=Imagenes("THD Voltaje L1",rutaImagenTHDVoltajeDistrL1)
            ImagenTHDVoltajeDistrL1.ConstruirImagen()
        with st.container():
            rutaImagenTHDVoltajeDistrL2=Datos["ArmonicosVoltaje"]["ArmonicosL2"]
            ImagenTHDVoltajeDistrL2=Imagenes("THD Voltaje L2",rutaImagenTHDVoltajeDistrL2)
            ImagenTHDVoltajeDistrL2.ConstruirImagen()
        with st.container():
            rutaImagenTHDVoltajeDistrL3=Datos["ArmonicosVoltaje"]["ArmonicosL3"]
            ImagenTHDVoltajeDistrL3=Imagenes("THD Voltaje L3",rutaImagenTHDVoltajeDistrL3)
            ImagenTHDVoltajeDistrL3.ConstruirImagen()
        