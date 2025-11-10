import streamlit as st
from Modelos import Descripciones,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()


def Descripcion():


    with st.container():
        rutaCentroCarga=Datos["Contexto"]["Descripcion"]
        DescripcionCentroCarga=Descripciones(rutaCentroCarga)
        DescripcionCentroCarga.ConstruirContenedor()
    # --- Diagrama Unifilar---
    with st.container():
        st.subheader("Diagrama Unifilar")
        rutaUnifilar=Datos["Unifilar"]
        ImagenUnifilar=Imagenes("",rutaUnifilar)
        ImagenUnifilar.ConstruirImagen()
    # --- Información General ---
    with st.expander(label="Datos de medición"):
        rutaDatosMedicion=Datos["Contexto"]["Medicion"]
        DescripcionDatos=Descripciones(rutaDatosMedicion)
        DescripcionDatos.ConstruirContenedor()

    with st.expander(label="Información del centro de carga"):
        rutaInfoCarga=Datos["Contexto"]["Informacion"]
        DescripcionInfoCarga=Descripciones(rutaInfoCarga)
        DescripcionInfoCarga.ConstruirContenedor()

    with st.expander(label="Información del medidor"):
        rutaMedidor=Datos["Contexto"]["Medidor"]
        DescripcionMedidor=Descripciones(rutaMedidor)
        DescripcionMedidor.ConstruirContenedor()
