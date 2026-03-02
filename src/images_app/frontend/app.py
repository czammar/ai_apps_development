import streamlit as st
import requests
from PIL import Image

st.title("Clasificador de Imágenes con ResNet")

uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

    if st.button("Clasificar"):
        response = requests.post(
            "http://localhost:8000/predict",
            files={"file": uploaded_file.getvalue()}
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Predicción:")
            st.write(f"**Objeto:** {result['label']}")
            st.write(f"**Confianza:** {result['confidence']:.4f}")
        else:
            st.error("Error en el backend")