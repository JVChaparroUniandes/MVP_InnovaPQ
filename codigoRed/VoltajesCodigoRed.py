import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def VoltajesCodigoRed():
    with st.container():

        with st.container():
            rutaTablaDescriptivasVoltaje=Datos["Voltaje"]["VoltajeTablaDescriptiva"]
            TablaDescriptivasVoltaje=Tabla("Descripción Voltajes RMS L-L",rutaTablaDescriptivasVoltaje)
            TablaDescriptivasVoltaje.construirContenedor()

        with st.expander(label="Voltajes RMS L-L"):
            rutaImagenVoltajeRMSMaximo=Datos["Voltaje"]["VoltajeRMSMaximo"]
            ImagenVoltajeRMSMaximo=Imagenes("Voltajes RMS Máximo",rutaImagenVoltajeRMSMaximo)
            ImagenVoltajeRMSMaximo.ConstruirImagen()

            rutaImagenVoltajeRMSMinimo=Datos["Voltaje"]["VoltajeRMSMinimo"]
            ImagenVoltajeRMSMinimo=Imagenes("Voltajes RMS Mínimo",rutaImagenVoltajeRMSMinimo)
            ImagenVoltajeRMSMinimo.ConstruirImagen()

            rutaImagenVoltajeRMSPromedio=Datos["Voltaje"]["VoltajeRMSPromedio"]
            ImagenVoltajeRMSPromedio=Imagenes("Voltajes RMS Promedio",rutaImagenVoltajeRMSPromedio)
            ImagenVoltajeRMSPromedio.ConstruirImagen()

        with st.expander(label="Distribución Voltaje L-L"):
            rutaImagenDistribucionLL=Datos["Voltaje"]["VoltajeDistrLL"]
            ImagenDistribucionLL=Imagenes("Distribución Voltaje L-L",rutaImagenDistribucionLL)
            ImagenDistribucionLL.ConstruirImagen()
        