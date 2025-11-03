import openpyxl
import pandas as pd
import streamlit as st
# --- Clases ---

class Tabla:
    def __init__(self,titulo,rutaDatos):
        self.titulo=titulo
        self.rutaDatos=rutaDatos

    def construirContenedor(self):
        df=pd.read_excel(io=self.rutaDatos,index_col=0)
        df=df.round(decimals=1)
        st.subheader(self.titulo)
        st.table(data=df)

class Descripciones:
    def __init__(self,rutaDatos):
        self.rutaDatos=rutaDatos
    
    def ConstruirContenedor(self):
        df=pd.read_excel(io=self.rutaDatos,header=None)
        df_datos = df.iloc[1:]
        st.subheader(df.iloc[0,0])
        for index,row in df_datos.iterrows():
            st.markdown(
                f'<p style="font-size: 18px; font-weight: bold;color:black;">{str(row[0])} </p>',
                unsafe_allow_html=True
                )
            st.write(str(row[1]))
                
class Imagenes:
    def __init__(self,titulo,rutaDatos):
        self.rutaDatos=rutaDatos
        self.titulo=titulo
    def ConstruirImagen(self):
        captionImg=st.markdown(
                f'<p style="font-size: 18px; font-weight: bold;color:black;">{self.titulo} </p>',
                unsafe_allow_html=True
                )
        col1, col2, col3 = st.columns([0.5,3,0.5])
        with col2:
            st.image(image=self.rutaDatos) 