from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/convert")
async def convert_to_grayscale(file: UploadFile = File(...)):
    # Leer imagen recibida
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Convertir a escala de grises
    gray_image = image.convert("L")
    
    # Guardar en memoria
    img_bytes = io.BytesIO()
    gray_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")