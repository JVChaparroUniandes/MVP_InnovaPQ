import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def FlickerCodigoRed():
    with st.container():
        st.subheader("Flicker")
        with st.container(horizontal=True):
                with st.container():
                    rutaTablaDescriptivasFlicker=Datos["Flicker"]["FlickerTablaPst"]
                    TablaDescriptivasFlicker=Tabla("Descripción PST",rutaTablaDescriptivasFlicker)
                    TablaDescriptivasFlicker.construirContenedor()
                with st.container():
                    rutaTablaCumplimientoFlicker=Datos["Flicker"]["FlickerTablaPlt"]
                    TablaCumplimientoFlicker=Tabla("Descripción PLT",rutaTablaCumplimientoFlicker)
                    TablaCumplimientoFlicker.construirContenedor()

        with st.expander(label="PST"):
            with st.container():
                rutaImagenFlickerPst=Datos["Flicker"]["FlickerPstSerieTiempo"]
                ImagenFlickerPst=Imagenes("Flicker Pst Serie de Tiempo",rutaImagenFlickerPst)
                ImagenFlickerPst.ConstruirImagen()

            with st.container():
                rutaImagenFlickerPstDistr=Datos["Flicker"]["FlickerDistrPst"]
                ImagenFlickerPstDistr=Imagenes("Distribución Flicker Pst",rutaImagenFlickerPstDistr)
                ImagenFlickerPstDistr.ConstruirImagen()

        with st.expander(label="PLT"):
            
            with st.container():
                rutaImagenFlickerPlt=Datos["Flicker"]["FlickerPltSerieTiempo"]
                ImagenFlickerPlt=Imagenes("Flicker Plt Serie de Tiempo",rutaImagenFlickerPlt)
                ImagenFlickerPlt.ConstruirImagen()
            
            with st.container():
                rutaImagenFlickerPltDistr=Datos["Flicker"]["FlickerDistrPlt"]
                ImagenFlickerPltDistr=Imagenes("Distribución Flicker Plt",rutaImagenFlickerPltDistr)
                ImagenFlickerPltDistr.ConstruirImagen()   
            