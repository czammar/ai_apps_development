import streamlit as st
import requests
from PIL import Image
import io

st.title("Convertidor de Imagen a Escala de Grises")

uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagen Original", use_column_width=True)

    if st.button("Convertir a Gris"):
        files = {"file": uploaded_file.getvalue()}
        
        response = requests.post(
            "http://localhost:8000/convert",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            st.image(img, caption="Imagen en Gris", use_column_width=True)
        else:
            st.error("Error procesando la imagen")