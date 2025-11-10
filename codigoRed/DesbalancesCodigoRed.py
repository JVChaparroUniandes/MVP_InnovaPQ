import streamlit as st
from Modelos import Tabla,Imagenes
from Servicio import Data


Servicio=Data()
Datos=Servicio.LeerDatos()

def DesbalancesCodigoRed():
    with st.container():
        with st.container(horizontal=True):
            with st.container():
                rutaTablaDescriptivasDesbalanceV=Datos["Desbalance"]["DesbalanceTablaDescriptivaVoltaje"]
                TablaDescriptivasDesbalanceV=Tabla("Descripción Desbalances Voltaje",rutaTablaDescriptivasDesbalanceV)
                TablaDescriptivasDesbalanceV.construirContenedor()
            with st.container():
                rutaTablaDescriptivasDesbalanceC=Datos["Desbalance"]["DesbalanceTablaDescriptivaCorriente"]
                TablaDescriptivasDesbalanceC=Tabla("Descripción Desbalances Corriente",rutaTablaDescriptivasDesbalanceC)
                TablaDescriptivasDesbalanceC.construirContenedor()

        with st.expander(label="Desbalance Voltajes"):
            with st.container():
                rutaImagenDesbalanceVoltaje=Datos["Desbalance"]["DesbalanceVoltajeSerieTiempo"]
                ImagenDesbalanceVoltaje=Imagenes("Desbalance de Voltaje",rutaImagenDesbalanceVoltaje)
                ImagenDesbalanceVoltaje.ConstruirImagen()
            with st.container():
                rutaDesbalanceDistrVoltaje=Datos["Desbalance"]["DesbalanceDistrVoltaje"]
                ImagenDesbalanceDistrVoltaje=Imagenes("Distribución Desbalance de Voltaje",rutaDesbalanceDistrVoltaje)
                ImagenDesbalanceDistrVoltaje.ConstruirImagen()
            
        with st.expander(label="Desbalance Corrientes"):

            with st.container():
                rutaImagenDesbalanceCorriente=Datos["Desbalance"]["DesbalanceCorrienteSerieTiempo"]
                ImagenDesbalanceCorriente=Imagenes("Desbalance de Corriente",rutaImagenDesbalanceCorriente)
                ImagenDesbalanceCorriente.ConstruirImagen()
            
            with st.container():
                rutaDesbalanceDistrCorriente=Datos["Desbalance"]["DesbalanceDistrCorriente"]
                ImagenDesbalanceDistrCorriente=Imagenes("Distribución Desbalance de Corriente",rutaDesbalanceDistrCorriente)
                ImagenDesbalanceDistrCorriente.ConstruirImagen()
            